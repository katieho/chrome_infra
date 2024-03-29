# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Antibody is meant to audit reviews for the Chromium project.

Example invocation: [TBD]
  ./run.py infra.tools.antibody <arguments>
"""

# This file is untested, keep as little code as possible in there.

import argparse
import logging
import os
import requests_cache
import sys

from infra.tools.antibody import antibody
import infra.tools.antibody.cloudsql_connect as csql
from infra.tools.antibody import code_review_parse
from infra.tools.antibody import git_commit_parser
import infra_libs.logs

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# https://storage.googleapis.com/chromium-infra-docs/infra/html/logging.html
LOGGER = logging.getLogger(__name__)


def main(argv):
  parser = argparse.ArgumentParser(
    prog="antibody",
    description=sys.modules['__main__'].__doc__)
  antibody.add_argparse_options(parser)
  infra_libs.logs.add_argparse_options(parser)
  args = parser.parse_args(argv)

  infra_libs.logs.process_argparse_options(args)

  if args.cache_path:
    requests_cache.install_cache(args.cache_path)
  else:
    requests_cache.install_cache(os.path.join(DATA_DIR, 'rietveld_cache'))

  # Do more processing here
  LOGGER.info('Antibody starting')
  with open(args.sql_password_file, 'r') as f:
    password = f.read().strip()
  connection, cc = csql.connect(password, args.database)
  checkout = args.git_checkout_path
  if args.parse_git_rietveld or args.run_antibody:
    antibody.setup_antibody_db(cc, os.path.join(
        DATA_DIR, 'ANTIBODY_DB_schema_setup.sql'), args.database)
    git_commit_parser.upload_to_sql(cc, checkout, args.since)
    git_commits_with_review_urls = git_commit_parser.get_urls_from_git_commit(
        cc)
    for review_url in git_commits_with_review_urls:
      # cannot get access into chromereview.googleplex.com
      if not any(host in review_url for host in (
          'chromereviews.googleplex',
      )):
        code_review_parse.add_code_review_data_to_db(review_url, cc, checkout)
    csql.commit(connection)
  if args.write_html or args.run_antibody:
    if not os.path.exists(args.output_dir_path):
      os.makedirs(args.output_dir_path)
    gitiles_prefix = antibody.get_gitiles_prefix(checkout)
    if not gitiles_prefix:
      gitiles_prefix = ''
    project_name = antibody.get_project_name(checkout).lower()
    antibody.generate_antibody_ui(cc, gitiles_prefix, project_name, args.since,
        args.output_dir_path, code_review_parse.get_tbr_no_lgtm(cc, 'author'),
        args.repo_list)
  csql.close(connection, cc)


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
