# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import endpoints
import webapp2

from findit_api import FindItApi
from handlers import build_failure
from handlers import check_duplicate_failures
from handlers import failure_log
from handlers import list_analyses
from handlers import monitor_alerts
from handlers import triage_analysis
from handlers import verify_analysis
from pipeline_wrapper import pipeline_status_ui


# This is for web pages.
web_pages_handler_mappings = [
    ('/build-failure', build_failure.BuildFailure),
    ('/check-duplicate-failures',
        check_duplicate_failures.CheckDuplicateFailures),
    ('/failure-log', failure_log.FailureLog),
    ('/list-analyses', list_analyses.ListAnalyses),
    ('/monitor-alerts', monitor_alerts.MonitorAlerts),
    ('/triage-analysis', triage_analysis.TriageAnalysis),
    ('/verify-analysis', verify_analysis.VerifyAnalysis),
]
web_application = webapp2.WSGIApplication(
    web_pages_handler_mappings, debug=False)


# This is for Cloud Endpoint apis.
api_application = endpoints.api_server([FindItApi])


# This is for appengine pipeline status pages.
pipeline_status_handler_mappings = [
    ('/_ah/pipeline/rpc/tree', pipeline_status_ui._TreeStatusHandler),
    ('/_ah/pipeline/rpc/class_paths', pipeline_status_ui._ClassPathListHandler),
    ('/_ah/pipeline/rpc/list', pipeline_status_ui._RootListHandler),
    ('/_ah/pipeline(/.+)', pipeline_status_ui._StatusUiHandler),
]
pipeline_status_application = webapp2.WSGIApplication(
    pipeline_status_handler_mappings, debug=False)
