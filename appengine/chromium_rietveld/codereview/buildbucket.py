# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Rietveld-BuildBucket integration module."""

import datetime
import json
import logging
import os
import urllib

from google.appengine.api import app_identity
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb

from django.conf import settings

from codereview import common
from codereview import models
from codereview import net

EPOCH = datetime.datetime.utcfromtimestamp(0)
BUILDBUCKET_HOSTNAME = (
    'cr-buildbucket-test.appspot.com' if common.IS_DEV
    else 'cr-buildbucket.appspot.com')
BUILDBUCKET_API_ROOT = (
    'https://%s/_ah/api/buildbucket/v1' % BUILDBUCKET_HOSTNAME)

# See tag conventions http://cr-buildbucket.appspot.com/#docs/conventions
BUILDSET_TAG_FORMAT = 'patch/rietveld/{hostname}/{issue}/{patch}'


class BuildBucketError(Exception):
  """Raised when a buildbucket operation failed."""
  pass


# TODO: make it a simple Python class. http://crbug.com/461900
class BuildbucketTryJobResult(models.TryJobResult):
  """A TryJobResult created from a BuildBucket build.

  Not stored, but only passed to pathset.html template.
  """

  build_id = ndb.StringProperty()

  @property
  def is_from_buildbucket(self):
    # Used in build_result.html template.
    return True

  @classmethod
  def convert_status_to_result(cls, build):
    """Converts build status to TryJobResult.result.

    See buildbucket docs here:
    https://cr-buildbucket.appspot.com/#/docs/build
    """
    status = build.get('status')
    if status == 'SCHEDULED':
      return cls.TRYPENDING

    if status == 'COMPLETED':
      if build.get('result') == 'SUCCESS':
        return cls.SUCCESS
      if build.get('result') == 'FAILURE':
        if build.get('failure_reason') == 'BUILD_FAILURE':
          return cls.FAILURE
      if build.get('result') == 'CANCELED':
        if build.get('cancelation_reason') == 'TIMEOUT':
          return cls.SKIPPED
      return cls.EXCEPTION

    if status == 'STARTED':
      return cls.STARTED

    logging.warning('Unexpected build %s status: %s', build.get('id'), status)
    return None

  @staticmethod
  def parse_tags(tag_list):
    """Parses a list of colon-delimited tags to a map."""
    return dict(tag.split(':', 1) for tag in tag_list)

  @classmethod
  def from_build(cls, build):
    """Converts a BuildBucket build to BuildBucketTryJobResult."""
    tags = cls.parse_tags(build.get('tags', []))
    result_details = load_json_dict_safe(build, 'result_details_json')
    parameters = load_json_dict_safe(build, 'parameters_json')
    properties = (
        result_details.get('properties') or parameters.get('properties'))
    if not isinstance(properties, dict):
      properties = {}

    def read_prop(name, expected_type):
      return dict_get_safe(properties, name, expected_type)

    requester = None
    requester_str = read_prop('requester', basestring)
    if requester_str:
      try:
        requester = users.User(requester_str)
      except users.UserNotFoundError:
        pass

    timestamp = timestamp_to_datetime(build.get('status_changed_ts'))
    if timestamp is None:
      logging.warning('Build %s has status_changed_ts=None', build['id'])

    return cls(
        id=build['id'],  # Required for to_dict() serialization.
        build_id=build['id'],
        url=dict_get_safe(build, 'url', basestring),
        result=cls.convert_status_to_result(build),
        master=tags.get('master'),
        builder=dict_get_safe(parameters, 'builder_name', basestring),
        slave=read_prop('slavename', basestring),
        buildnumber=read_prop('buildnumber', int),
        reason=read_prop('reason', basestring),
        revision=read_prop('revision', basestring),
        timestamp=timestamp,
        clobber=read_prop('clobber', bool),
        tests=read_prop('testfilter', list) or [],
        project=read_prop('project', basestring),
        requester=requester,
        category=read_prop('category', basestring),
        build_properties=json.dumps(properties, sort_keys=True),
    )


@ndb.tasklet
def get_builds_for_patchset_async(project, issue_id, patchset_id):
  """Queries BuildBucket for builds associated with the patchset.

  Requests for max 500 builds and does not check "next_cursor". Currently if
  more than 100 builds are requested, only 100 are returned. Presumably there
  will be no patchsets with >100 builds.

  Returns:
    A list of buildbucket build dicts.
  """
  # See tag conventions http://cr-buildbucket.appspot.com/#docs/conventions .
  hostname = common.get_preferred_domain(project, default_to_appid=False)
  if not hostname:
    logging.error(
        'Preferred domain name for this app is not set. '
        'See PREFERRED_DOMAIN_NAMES in settings.py: %r', hostname)
    raise ndb.Return([])

  buildset_tag = BUILDSET_TAG_FORMAT.format(
      hostname=hostname,
      issue=issue_id,
      patch=patchset_id,
  )
  params = {
      'max_builds': 500,
      'tag': 'buildset:%s' % buildset_tag,
  }

  url = '%s/search' % BUILDBUCKET_API_ROOT
  logging.info(
      'Fetching builds for patchset %s/%s. Buildset: %s',
      issue_id, patchset_id, buildset_tag)
  try:
    resp = yield net.json_request_async(
        url, params=params,
        scopes='https://www.googleapis.com/auth/userinfo.email')
  except net.NotFoundError as ex:
    logging.error(
        'Buildbucket returned 404 unexpectedly. Body: %s', ex.response)
    raise
  if 'error' in resp:
    bb_error = resp.get('error', {})
    raise BuildBucketError(
        'BuildBucket responded with error (reason %s): %s' % (
            bb_error.get('reason', 'no-reason'),
            bb_error.get('message', 'no-message')))
  raise ndb.Return(resp.get('builds') or [])


@ndb.tasklet
def get_try_job_results_for_patchset_async(project, issue_id, patchset_id):
  """Returns try job results stored on buildbucket."""
  builds = yield get_builds_for_patchset_async(project, issue_id, patchset_id)
  results = []
  for build in builds:
    try_job_result = BuildbucketTryJobResult.from_build(build)
    if not try_job_result.builder:
      logging.info(
          'Build %s does not have a builder' % try_job_result.build_id)
      continue
    results.append(try_job_result)
  raise ndb.Return(results)


################################################################################
## Utility functions.


def load_json_dict_safe(container_dict, key_name):
  """Tries to parse a json-encoded dict, otherwise returns {}."""
  possibly_json = container_dict.get(key_name)
  if not possibly_json:
    return {}
  try:
    result = json.loads(possibly_json)
    if result is None:
      return {}
    if not isinstance(result, dict):
      logging.warning(
          '%s expected to be a dict. Got %s instead', key_name, result)
      result = {}
  except ValueError as ex:
    logging.warning(
        'Could not parse %s as json: %s.\nInput: %s',
        key_name, ex, possibly_json)
    result = {}
  return result


def dict_get_safe(container_dict, key_name, expected_type):
  """Returns value if it is an instance of |expected_type|, otherwise None."""
  value = container_dict.get(key_name)
  if value is not None and not isinstance(value, expected_type):
    logging.warning(
        'Unexpected type for %s. Expected type: %s. Value: %r.',
        key_name, expected_type.__name__, value,
    )
    return None
  return value


def timestamp_to_datetime(timestamp):
  if timestamp is None:
    return None
  if isinstance(timestamp, basestring):
    timestamp = int(timestamp)
  return EPOCH + datetime.timedelta(microseconds=timestamp)
