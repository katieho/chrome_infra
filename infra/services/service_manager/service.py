# Copyright (c) 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import errno
import json
import logging
import os.path
import platform
import signal
import sys
import time

import psutil

from infra.libs.service_utils import daemon
from infra.services.service_manager import version_finder

LOGGER = logging.getLogger(__name__)


class ServiceException(Exception):
  """Raised if the child process couldn't be started correctly."""


class ProcessStateError(Exception):
  """Raised by get_running_process_state.

  Errors of this type can either be routine errors because the process is not
  running or unexpected errors (failed to parse the state file).  The former
  inherit ProcessNotRunning, the latter inherit UnexpectedProcessStateError."""


class ProcessNotRunning(ProcessStateError):
  pass


class StateFileNotFound(ProcessNotRunning):
  pass


class ProcessHasDifferentStartTime(ProcessNotRunning):
  pass


class UnexpectedProcessStateError(ProcessStateError):
  pass


class StateFileOpenError(UnexpectedProcessStateError):
  pass


class StateFileParseError(UnexpectedProcessStateError):
  pass


def _read_starttime(pid):  # pragma: no cover
  try:
    ret = int(psutil.Process(pid).create_time())
  except (psutil.NoSuchProcess, psutil.AccessDenied):
    return None

  if platform.system() == 'Linux':
    # On Linux psutil adds the btime from /proc/stat to the create_time.
    # Unfortunately this value isn't constant and can drift by 1 second, so
    # subtract it again to ensure different service_manager processes see the
    # same create_times.  See crbug/509493.
    ret -= psutil.BOOT_TIME

  return ret


class ProcessState(object):
  """Reads and writes process state to files.

  A ProcessState object will contain information about a running process
  accessible using the 'pid', 'starttime', etc. attributes.
  """

  def __init__(self, pid=None, starttime=None, version=None, args=None):
    self.pid = None
    if pid is not None:
      self.pid = int(pid)

    self.starttime = None
    if starttime is not None:
      self.starttime = int(starttime)

    self.version = version
    self.args = args

  @classmethod
  def from_file(cls, filename):
    """Reads a state file from disk."""

    if not os.path.isfile(filename):
      raise StateFileNotFound(filename)

    try:
      with open(filename) as fh:
        data = json.load(fh)
        pid = data['pid']
        starttime = data['starttime']  # pragma: no cover (coverage bug??)
    except IOError as ex:
      raise StateFileOpenError(filename, ex)
    except Exception as ex:
      raise StateFileParseError(filename, ex)

    # Check that the same process is still on this pid.
    pid_state = cls.from_pid(pid)

    if not pid_state.is_starttime_near(starttime):
      raise ProcessHasDifferentStartTime(
          filename, pid, pid_state.starttime, starttime)

    return cls(pid=pid,
               starttime=starttime,
               version=data.get('version'),
               args=data.get('args'))

  @classmethod
  def from_pid(cls, pid):
    """Checks if the PID is running and returns a minimal ProcessState object.

    If the process is running the returned object will only have the pid and
    starttime properties set.
    """

    starttime = _read_starttime(pid)
    if starttime is None:
      raise ProcessNotRunning(None, pid)

    return cls(pid=pid, starttime=starttime)

  def write_to_file(self, filename):
    contents = json.dumps({
        'pid': self.pid,
        'starttime': self.starttime,
        'version': self.version,
        'args': self.args,
    })
    LOGGER.info('Writing state file %s: %s', filename, contents)

    with open(filename, 'w') as fh:
      fh.write(contents)

  def is_starttime_near(self, other):
    return abs(self.starttime - int(other)) < 10


class Service(object):
  """Controls a running service process.

  Starts and stops the process, checks whether it is running, and creates and
  deletes its state file in the state_directory.

  State files are like UNIX PID files, except they also contain the starttime
  (read from /proc/$PID/stat) of the process to protect against the race
  condition of a different process reusing the same PID.
  """

  def __init__(self, state_directory, service_config, time_fn=time.time,
               sleep_fn=time.sleep):
    """
    Args:
      state_directory: A file will be created in this directory (with the same
          name as the service) when it is running containing its PID and
          starttime.
      service_config: A dictionary containing the service's config.  See README
          for a description of the fields.
    """

    self.config = service_config
    self.name = service_config['name']
    self.root_directory = service_config['root_directory']
    self.tool = service_config['tool']

    self.args = service_config.get('args', [])
    self.stop_time = int(service_config.get('stop_time', 10))

    self._state_file = os.path.join(state_directory, self.name)
    self._time_fn = time_fn
    self._sleep_fn = sleep_fn

  def get_running_process_state(self):
    """Returns a ProcessState object about about the process.

    Raises some subclass of ProcessStateError if the process is not running.
    """

    return ProcessState.from_file(self._state_file)

  def has_version_changed(self, state):
    """Returns True if the version has changed since the process started."""

    if state.version is None:
      return False

    return state.version != version_finder.find_version(self.config)

  def has_args_changed(self, state):
    """Returns True if the args in the config are different to when the process
    started."""

    if state.args is None:
      return False

    return state.args != self.args

  def start(self):
    """Starts the service if it's not running already.

    Does nothing if the service is running already.  Raises ServiceException if
    the process couldn't be started.
    """

    try:
      self.get_running_process_state()
    except ProcessStateError:
      pass
    else:
      return  # Running already.

    LOGGER.info("Starting service %s", self.name)

    pipe_r, pipe_w = os.pipe()
    child_pid = os.fork()
    if child_pid == 0:
      os.close(pipe_r)
      try:
        self._start_child(os.fdopen(pipe_w, 'w'))
      finally:
        os._exit(1)
    else:
      os.close(pipe_w)
      self._start_parent(os.fdopen(pipe_r, 'r'), child_pid)

  def stop(self):
    """Stops the service if it is currently running.

    Does nothing if it's not running.
    """

    try:
      state = self.get_running_process_state()
    except ProcessStateError:
      return  # Not running.

    if not self._signal_and_wait(state, signal.SIGTERM, self.stop_time):
      self._signal_and_wait(state, signal.SIGKILL, None)

    LOGGER.info("Service %s stopped", self.name)

    # Remove the state file.
    os.unlink(self._state_file)

  def _start_child(self, pipe):
    """The part of start() that runs in the child process.

    Daemonises the current process, writes the new PID to the pipe, and execs
    the service executable.
    """

    # Detach from the parent and close all FDs except that of the pipe.
    daemon.become_daemon(keep_fds={pipe.fileno()})

    # Write our new PID to the pipe and close it.
    json.dump({'pid': os.getpid()}, pipe)
    pipe.close()

    # Exec the service.
    runpy = os.path.join(self.root_directory, 'run.py')
    os.execv(runpy, [runpy, self.tool] + self.args)

  def _start_parent(self, pipe, child_pid):
    """The part of start() that runs in the parent process.

    Waits for the child to start and writes a state file for the process.
    """

    # Read the data from the pipe.  The daemon process will close this pipe
    # before starting the service, or it will be closed when the child exits.
    data = pipe.read()

    # Reap the child we forked.
    _, exit_status = os.waitpid(child_pid, 0)
    if exit_status != 0:
      raise ServiceException(
          'Failed to start %s: child process exited with %d' % (
              self.name, exit_status))

    # Try to parse the JSON sent by the daemon process.
    try:
      data = json.loads(data)
    except Exception:
      raise ServiceException(
          'Failed to start %s: daemon process didn\'t send a valid PID' %
          self.name)

    self._write_state_file(data['pid'])
    LOGGER.info("Service %s started with PID %d", self.name, data['pid'])

  def _write_state_file(self, pid):
    try:
      state = ProcessState.from_pid(pid)
    except ProcessStateError as ex:
      raise ServiceException(
          'Failed to start %s: daemon process exited (%r)' % (self.name, ex))

    state.version = version_finder.find_version(self.config)
    state.args = self.args
    state.write_to_file(self._state_file)

  def _signal_and_wait(self, state, sig, wait_timeout):
    """Sends a signal to the given process, and optionally waits for it to exit.

    Args:
      state: A ProcessState object of the process to signal.
      sig: The signal number to send (see the constants in the signal module).
      wait_timeout: Time in seconds to wait for this process to exit after
          sending the signal, or None to return immediately.

    Returns:
      False if the process was still running after the timeout, or True if the
      process exited within the timeout, or timeout was None.
    """

    LOGGER.info("Sending signal %d to %s with PID %d",
                sig, self.name, state.pid)
    try:
      os.kill(state.pid, sig)
    except OSError as ex:
      if ex.errno == errno.ESRCH:
        # The process exited before we could kill it.
        return True
      raise

    if wait_timeout is not None:
      return self._wait_with_timeout(state, wait_timeout)

    return True

  def _wait_with_timeout(self, state, timeout):
    """Waits for the process to exit."""

    deadline = self._time_fn() + timeout
    while self._time_fn() < deadline:
      try:
        new_state = ProcessState.from_pid(state.pid)
      except ProcessStateError:
        return True  # Not running
      if not new_state.is_starttime_near(state.starttime):
        return True

      self._sleep_fn(0.1)
    return False


class OwnService(Service):
  """A special service that represents the service_manager itself.

  Makes the get_running_process_state() functionality available for the
  service_manager process.
  """

  def __init__(self, state_directory, root_directory, **kwargs):
    super(OwnService, self).__init__(state_directory, {
        'name': 'service_manager',
        'tool': '',
        'root_directory': root_directory,
    }, **kwargs)
    self._state_directory = state_directory

  def start(self):
    """Writes a state file, returns False if we're already running."""

    # Use a flock here to avoid a race condition where two service_managers
    # start at the same time and both write their own state file.
    try:
      with daemon.flock('service_manager.flock', self._state_directory):
        try:
          self.get_running_process_state()
        except ProcessStateError:
          pass
        else:
          return False  # already running

        self._write_state_file(os.getpid())
        return True
    except daemon.LockAlreadyLocked:
      return False

  def stop(self):
    raise NotImplementedError
