#!/usr/bin/env python
# Copyright (c) 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Download and run node.js."""

import optparse
import os
import shutil
import sys
import subprocess
import tarfile
import tempfile
import urllib2

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_VERSION = '0.12.2'
BUCKET = 'chromium-infra-bins'


def install_latest_node_js(version, tmp_dir):
  target_dir = os.path.join(THIS_DIR, 'runtimes', version)
  version_file = os.path.join(target_dir, 'VERSION')

  if sys.platform == 'win32':
    bin_location = os.path.join(target_dir, 'node.exe')
  else:
    bin_location = os.path.join(target_dir, 'bin', 'node')

  # We assume that, if the VERSION file exists, then the installation is good.
  if os.path.exists(version_file):
    with open(version_file, 'r') as f:
      if f.read() == version:
        return bin_location

  # TODO(hinoka): This probably doesn't work that well on Windows...
  shutil.rmtree(target_dir, ignore_errors=True)

  # Get the target name correct.
  if sys.platform == 'win32':
    target = 'node.exe'
  elif sys.platform == 'darwin':
    target = 'node-v%s-darwin-x86.tar.gz' % version
  elif sys.platform == 'linux2':
    target = 'node-v%s-linux-x86.tar.gz' % version
  else:
    raise Exception('Unrecognized platform %s' % sys.platform)

  dest = os.path.join(tmp_dir, 'node_download')
  url = 'https://storage.googleapis.com/%s/node/%s/%s' % (
      BUCKET, version, target)
  print('Fetching %s' % url)
  u = urllib2.urlopen(url)
  with open(dest, 'wb') as f:
    while True:
      chunk = u.read(2 ** 20)
      if not chunk:
        break
      f.write(chunk)

  if sys.platform != 'win32':
    # The Windows version comes as a self contained executable, the other
    # versions come as a tar.gz that needs to be extracted.
    with tarfile.open(dest, 'r:gz') as f:
      f.extractall(path=tmp_dir)
    shutil.move(os.path.join(tmp_dir, target[:-len('.tar.gz')]), target_dir)
    os.remove(dest)
  else:
    os.mkdir(target_dir)
    shutil.move(dest, bin_location)

  with open(version_file, 'w') as f:
    f.write(version)

  return bin_location


def main():
  parser = optparse.OptionParser(prog='python -m %s' % __package__)
  parser.add_option('-v', '--version', default=DEFAULT_VERSION,
                    help='Specify a version, default %s' % DEFAULT_VERSION)
  options, args = parser.parse_args()

  try:
    tmp_dir = tempfile.mkdtemp(dir=THIS_DIR)
    bin_location = install_latest_node_js(options.version, tmp_dir)
  finally:
    if os.path.exists(tmp_dir):
      shutil.rmtree(tmp_dir)

  return subprocess.call([bin_location,] + args)


if __name__ == '__main__':
  sys.exit(main())
