# Copyright 2013 Google Inc.
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

import os

from google.appengine.api import app_identity

from django.conf import settings

IS_DEV = os.environ['SERVER_SOFTWARE'].startswith('Dev')  # Development server


def get_preferred_domain(project=None, default_to_appid=True):
  """Returns preferred domain for a given project."""
  try:
    projects_prefs = settings.PREFERRED_DOMAIN_NAMES[settings.APP_ID]
  except KeyError:
    if default_to_appid:
      return '%s.appspot.com' % app_identity.get_application_id()
    return None
  return projects_prefs.get(project, projects_prefs[None])
