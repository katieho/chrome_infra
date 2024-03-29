# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.


# Represent status of the analysis of a Chromium waterfall build failure.
PENDING = 0
ANALYZING = 10
ANALYZED = 70
ERROR = 80



STATUS_TO_DESCRIPTION = {
    PENDING: 'Pending',
    ANALYZING: 'Analyzing',
    ANALYZED: 'Analyzed',
    ERROR: 'Error'
}
