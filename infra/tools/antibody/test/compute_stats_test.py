# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import datetime
import unittest

from infra.tools.antibody import compute_stats


class Cursor(object):
  def execute(self, arg):
    pass

  def fetchall(self):
    results = (('https://codereview.chromium.org/1148323006',
                datetime.datetime(2015, 5, 28, 16, 8, 33),
                'suppress-uninit-error-from-sessions-SessionBackend-'
                'AppendCommandsToFile',
                'bf1cf11bb721eb52bf46868cb831afd1f53567af'),
               ('https://codereview.chromium.org/1159593004',
                datetime.datetime(2015, 6, 1, 3, 37, 20),
                'Revert-of-Converted-some-extension-browser-tests-into-using-'
                'event-pages-patchset-1-id-60001-of-https-codereview.chromium.'
                'org-1108133002',
                'cda8c938f06f9955ac895099d05a9db3b61f3ab5'),
               ('https://codereview.chromium.org/1156073004',
                datetime.datetime(2015, 5, 26, 20, 52, 41),
                'MemSheriff-Expand-suppressions-for-sqlite3-uninitialized-'
                'reads',
                'f48757cfe41e83e770095253b90775eb70f024b3'),
               ('https://codereview.chromium.org/1124083006',
                datetime.datetime(2015, 5, 20, 0, 26, 31),
                'Revert-of-Temporarily-disable-a-webgl-conformance-test-on-'
                'D3D9-only.-patchset-1-id-1-of-https-codereview.chromium.org-'
                '1135333004',
                '0b0b636093a7dbb56cc8712e2263b1c9a1ad8079'))
    return results

class TestComputeStats(unittest.TestCase):
  def setUp(self):
    self.cc = Cursor()

  def test_ratio_calculator(self):
    reg_num = [['2014-01', 1], ['2014-02', 3], ['2014-07', 5]]
    reg_den = [['2014-07', 10], ['2014-02', 6], ['2014-01', 9]]
    reg_ratio = compute_stats.ratio_calculator(reg_num, reg_den)
    self.assertEqual(reg_ratio,
                     [['2014-01', 0.111], ['2014-02', 0.5], ['2014-07', 0.5]])

    zero_num = [['2014-01', 1], ['2014-02', 0], ['2014-07', 5]]
    zero_den = [['2014-07', 10], ['2014-02', 0], ['2014-01', 0]]
    zero_ratio = compute_stats.ratio_calculator(zero_num, zero_den)
    self.assertEqual(zero_ratio,
                     [['2014-01', 0], ['2014-02', 0], ['2014-07', 0.5]])

    missing_num = [['2014-01', 1], ['2014-02', 3], ['2014-07', 5]]
    missing_den = [['2014-02', 3], ['2014-07', 10]]
    missing_ratio = compute_stats.ratio_calculator(missing_num, missing_den)
    self.assertEqual(missing_ratio,
                     [['2014-02', 1.0], ['2014-07', 0.5]])

    extra_num = [['2014-01', 1], ['2014-02', 3], ['2014-07', 5]]
    extra_den = [['2014-02', 3], ['2015-07', 5], ['2015-07', 5]]
    extra_ratio = compute_stats.ratio_calculator(extra_num, extra_den)
    self.assertEqual(extra_ratio, [['2014-02', 1.0]])

  def test_totaled_ratio_calculator(self):
    ratio = compute_stats.totaled_ratio_calculator(3, 7)
    self.assertEqual(ratio, 0.429)
    zero_ratio = compute_stats.totaled_ratio_calculator(5, 0)
    self.assertEqual(zero_ratio, 0)

  def test_totaled_tbr_no_lgtm(self):
    sql_time_specification = 'DATEDIFF(git_commit.timestamp, NOW()) < 0'
    total_num, output = compute_stats.totaled_tbr_no_lgtm(self.cc,
        sql_time_specification)
    self.assertEqual(total_num, 4)
    self.assertItemsEqual(output,
        [['https://codereview.chromium.org/1148323006',
          '2015-05-28 16:08:33',
          'suppress uninit error from sessions SessionBackend '
          'AppendCommandsToFile',
          'bf1cf11bb721eb52bf46868cb831afd1f53567af'],
         ['https://codereview.chromium.org/1159593004',
          '2015-06-01 03:37:20',
          'Revert of Converted some extension browser tests into using '
          'event pages patchset 1 id 60001 of https codereview.chromium.'
          'org 1108133002',
          'cda8c938f06f9955ac895099d05a9db3b61f3ab5'],
         ['https://codereview.chromium.org/1156073004',
          '2015-05-26 20:52:41',
          'MemSheriff Expand suppressions for sqlite3 uninitialized reads',
          'f48757cfe41e83e770095253b90775eb70f024b3'],
         ['https://codereview.chromium.org/1124083006',
          '2015-05-20 00:26:31',
          'Revert of Temporarily disable a webgl conformance test on '
          'D3D9 only. patchset 1 id 1 of https codereview.chromium.org '
          '1135333004',
          '0b0b636093a7dbb56cc8712e2263b1c9a1ad8079']])