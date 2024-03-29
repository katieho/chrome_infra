# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from google.appengine.ext import ndb

from model.build_run import BuildRun

# A particular occurance of a single flake occuring.
class FlakeOccurance(ndb.Model):
  # step name, i.e. browser_tests
  name = ndb.StringProperty(required=True)
  # failre, i.e. FooTest.Bar
  failure = ndb.StringProperty(required=True)


# Represents a patchset with a successful and failed try run for a particular
# builder. The flaky failed run can have multiple different flakes that cause
# it to turn red, each represented by a FlakeOccurance.
class FlakyRun(ndb.Model):
  failure_run = ndb.KeyProperty(BuildRun, required=True)
  # A copy of failure_run.time_finished to reduce lookups.
  failure_run_time_finished = ndb.DateTimeProperty(required=True)
  success_run = ndb.KeyProperty(BuildRun, required=True)
  flakes = ndb.StructuredProperty(FlakeOccurance, repeated=True)
  comment = ndb.StringProperty()

# Represents a step that flakes. The name could be a test_suite:test name (i.e.
# unit_tests:FooTest), a ninja step in case of compile flake, etc... This entity
# groups together all the occurrences of this flake, with each particular
# instance of a flake being represented by a FlakyRun.
class Flake(ndb.Model):
  name = ndb.StringProperty(required=True)
  occurrences = ndb.KeyProperty(FlakyRun, repeated=True)
  comment = ndb.StringProperty(default='')

  # Used so we can quickly query and sort by number of occurrances per time
  # range.
  count_hour = ndb.IntegerProperty(default=0)
  count_day = ndb.IntegerProperty(default=0)
  count_week = ndb.IntegerProperty(default=0)
  count_month = ndb.IntegerProperty(default=0)
  count_all = ndb.IntegerProperty(default=0)
  last_time_seen = ndb.DateTimeProperty()

  # This is needed to allow the query in update_flake_date_flags to be fast.
  last_hour = ndb.BooleanProperty(default=False)
  last_day = ndb.BooleanProperty(default=False)
  last_week = ndb.BooleanProperty(default=False)
  last_month = ndb.BooleanProperty(default=False)