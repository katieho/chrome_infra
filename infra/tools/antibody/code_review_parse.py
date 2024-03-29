# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import datetime
import logging
import re
import requests
from simplejson.scanner import JSONDecodeError
import subprocess
from urlparse import urlparse

import infra.tools.antibody.cloudsql_connect as csql
from infra.tools.antibody.static.third_party import gerrit_util


# https://chromium.googlesource.com/infra/infra/+/master/infra_libs/logs/README.md
LOGGER = logging.getLogger(__name__)

time_format = '%Y-%m-%d %H:%M:%S'
KNOWN_RIETVELD_INSTANCES = [
    'chromereviews.googleplex.com',
    'chromiumcodereview-hr.appspot.com',
    'chromiumcodereview.appspot.com',
    'codereview.appspot.com',
    'codereview.chromium.org',
    'skia-codereview-staging.appspot.com',
    'skia-codereview-staging2.appspot.com',
    'skia-codereview-staging3.appspot.com',
]
KNOWN_GERRIT_INSTANCES = [
    'chromium-review.googlesource.com',
]

def extract_code_review_json_data(review_url, cc, git_checkout_path):
  if any(hostname in review_url for hostname in KNOWN_RIETVELD_INSTANCES):
    return _extract_json_data_from_rietveld(review_url)
  elif any(hostname in review_url for hostname in KNOWN_GERRIT_INSTANCES):
    return _extract_json_data_from_gerrit(review_url, cc, git_checkout_path)
  else:
    LOGGER.error('unknown code review instance: %s' % review_url)


def _extract_json_data_from_rietveld(rietveld_url):
  """Extracts json data from an issue of a rietveld instance

  Args:
    rietveld_url(str): rietveld url formatted 'https://hostname/issuenum'

  Return:
    Dictionary containing information from rietveld about the specific 
    issue linked in rietveld_url. 

    * It is important to note that not all fields existed in at the time of a 
    given CL's existence, so the data is not all 100% reliable. Known false 
    cases are starred below.

    Most relevant keys:
      - 'owner_email': email address of the owner
      - 'created': timestamp issue was created
      - 'cc': list of cc'ed email addresses
      - 'reviewers': list of reviewers' email addresses
      - 'messages': dict with the following relevant keys:
        - *'patchset': latest patchset when message was sent. Note: for some
            older CLs, this value is null for all messages.
        - 'sender': message author email address
        - 'approval': boolean for whether or not the message contained 'lgtm'
        - 'date': timestamp message was sent
        - 'text': str containing contents of the message
        - 'auto_generated': boolean for whether or not the message was 
            autogenerated. Note: messages from commit-bot are not considered
            autogenerated.
        - 'disapproval': boolean for whether or not the message contained 
            'not lgtm'
        - 'issue_was_closed': boolean for whether or not the issue was closed
            at the time it was sent. Note: this is true for 'Patchset 
            committed' messages
      - 'patchsets': list of patchset IDs that still exist on Rietveld at time
          of request
      - 'modified': timestamp the CL was last modified
  """
  url_components = urlparse(rietveld_url)
  json_data_url = '%s://%s/api%s?messages=true' % (url_components.scheme,
                  url_components.netloc, url_components.path)
  logging.info('Sending request to: %s', json_data_url)
  response = requests.get(json_data_url)
  if (response.status_code == requests.codes.ok):
    try:
      return response.json()
    except JSONDecodeError:  # pragma: no cover
      LOGGER.error('json parse failed for url: %s' % rietveld_url)
      raise
  else:  # pragma: no cover
    LOGGER.info('unable to access: %s' % rietveld_url)
    response.raise_for_status()


def _extract_json_data_from_gerrit(gerrit_url, cc, git_checkout_path):
  """Extracts json data from an issue of a gerrit instance

  Args:
    gerrit_url(str): gerrit url formatted 'https://hostname/issuenum'
    cc(Cursor): cursor to the database with extra info on 

  Return:
    Dictionary containing informationon from gerrit about the specific
    issue linked in gerrit_url

    Most relevant keys:
      - 'owner': dict with name and email of owner
      - 'created': timestamp issue was created
      - 'updated': timestamp issue was last updated
      - 'labels': dict with the following relevant keys:
        - 'Code Review': dict with the following relevant keys:
          - 'approved': dict with name and email of approver
          - 'all': list of dicts with name and email of all users marked for
                   review, as well as review result and time that user last 
                   updated review status or commented
          - 'values': dict of possible numerical rating values and meanings
      - 'messages': list of messages, each represented as dicts with the
                    following relevant keys:
        - 'author': dict with name and email of the author of the comment
        - 'date': timestamp the message was posted
        - 'message': str containing contents of the message
  """
  url_components = urlparse(gerrit_url)
  cc.execute(""" SELECT hash 
      FROM git_commit
      WHERE review_url = '%s'""" % gerrit_url)
  git_hash = cc.fetchone()[0]
  commit_message = subprocess.check_output(['git', 'show', git_hash, 
                                            '--format=%b'],
                                            cwd=git_checkout_path)
  change_id = None
  match_count = 0
  for line in commit_message.splitlines():
    if line.startswith('Change-Id: '):
      match_count += 1
      if not change_id:
        change_id = line[len('Change-Id: '):]
  if match_count > 1:
    LOGGER.warn('Multiple lines beginning with Change-Id for %s' 
                    % gerrit_url)
  change_detail = gerrit_util.GetChangeDetail(url_components.netloc, change_id)
  if change_detail:
    return change_detail
  else:
    LOGGER.error('could not get change detail for: %s' % gerrit_url)


def to_canonical_review_url(review_url):
  review_url = review_url.strip('.')
  if 'chromiumcodereview.appspot.com' in review_url:
    return review_url.replace('chromiumcodereview.appspot.com',
                              'codereview.chromium.org')
  if 'chromiumcodereview-hr.appspot.com' in review_url:
    return review_url.replace('chromiumcodereview-hr.appspot.com',
                              'codereview.chromium.org')
  return review_url


def add_code_review_data_to_db(review_url, cc, git_checkout_path):
  review_url = to_canonical_review_url(review_url)
  try:
    json_data = extract_code_review_json_data(review_url, cc, git_checkout_path)
  except JSONDecodeError:  # pragma: no cover
    return
  if any(hostname in review_url for hostname in KNOWN_RIETVELD_INSTANCES):
    db_data = _get_rietveld_data_for_review(review_url, json_data)
    csql.write_to_review(cc, db_data)
    db_data_all = _get_rietveld_data_for_review_people(review_url, json_data)
    csql.write_to_review_people(cc, db_data_all)
  elif any(hostname in review_url for hostname in KNOWN_GERRIT_INSTANCES):
    db_data = _get_gerrit_data_for_review(review_url, json_data)
    csql.write_to_review(cc, db_data)
    db_data = _get_gerrit_data_for_review_people(review_url, json_data)
    csql.write_to_review_people(cc, db_data)
  else:
    LOGGER.error('unknown code review instance: %s' % review_url)


def _get_rietveld_data_for_review(rietveld_url, json_data):
  curr_time = datetime.datetime.utcnow()
  committed_timestamp = None
  patchset_still_exists = None
  for message in json_data['messages']:
    if ('committed' in message['text'].lower() and
        message['issue_was_closed']):
      committed_timestamp = message['date'].split('.')[0]
      if message['patchset'] in json_data['patchsets']:
        patchset_still_exists = True
      else:
        patchset_still_exists = False
  # TODO(ksho): insert data for reverts/project id
  db_data = (rietveld_url, curr_time, committed_timestamp,
             patchset_still_exists, None, None)
  return db_data


def _get_gerrit_data_for_review(gerrit_url, json_data):
  curr_time = datetime.datetime.utcnow()
  committed_timestamp = None
  # merged patchsets cannot be deleted in gerrit
  patchset_still_exists = True
  for message in json_data['messages']:
    # TODO(ksho): write better check to detect generated committed message
    # by using more explicit checks for bots, checking all requirements
    # for commit and all changes due to commit, 
    if (
        json_data['status'] == 'MERGED'
        and
        ('author' not in message.keys() or
         'bot' in message['author']['name'].lower())
        and
        any(commit_text in message['message'].lower() for commit_text in
            (
              'cherry-picked',
              'cherry picked',
              'merged',
              'pushed',
            )
          )
        ):
      committed_timestamp = message['date'].split('.')[0]
  # TODO(ksho): insert data for reverts/project id
  db_data = (gerrit_url, curr_time, committed_timestamp,
             patchset_still_exists, None, None)
  return db_data


def _get_rietveld_data_for_review_people(rietveld_url, json_data):
  curr_time = datetime.datetime.utcnow()
  db_data_all = []

  people = []
  people.append([json_data['cc'], 'cc'])
  people.append([json_data['reviewers'], 'reviewer'])
  people.append([[json_data['owner_email'],], 'owner'])
  time_submitted = json_data['created'].split('.')[0]
  for person_list, typ in people:
    for person_email in person_list:
      db_data = (person_email, rietveld_url, time_submitted, curr_time, typ)
      db_data_all.append(db_data)
  for message in json_data['messages']:
    if message['approval']:
      time_commented = message['date'].split('.')[0]
      db_data = (message['sender'], rietveld_url, time_commented, curr_time,
                 'lgtm')
      db_data_all.append(db_data)
    elif message['disapproval']:
      time_commented = message['date'].split('.')[0]
      db_data = (message['sender'], rietveld_url, time_commented, curr_time,
                'not lgtm')
      db_data_all.append(db_data)
  return db_data_all


def _get_gerrit_data_for_review_people(gerrit_url, json_data):
  curr_time = datetime.datetime.utcnow()
  db_data_all = []

  time_submitted = json_data['created'].split('.')[0]
  db_data_all.append((json_data['owner']['email'], gerrit_url,
                      time_submitted, curr_time, 'owner'))
  people = json_data['labels']['Code-Review']['all']
  for person in people:
    person_email = person['email']
    if 'commit-bot@chromium.org' in person_email:  # pragma: no cover
      continue
    # in gerrit "+2" means "Looks good to me, approved"
    if person['value'] == 2:
      db_data_all.append((person_email, gerrit_url,
                          person['date'].split('.')[0], curr_time, 'lgtm'))
    # in gerrit "-2" means "Do not submit"
    elif person['value'] == -2:
      db_data_all.append((person_email, gerrit_url,
                          person['date'].split('.')[0], curr_time, 'not lgtm'))
    db_data = (person_email, gerrit_url, time_submitted, curr_time, 'reviewer')
    db_data_all.append(db_data)
  return db_data_all


def get_tbr_no_lgtm(cc, commit_people_type):
  cc.execute("""SELECT review.review_url, git_commit.timestamp,
      git_commit.subject, commit_people.people_email_address, git_commit.hash
      FROM review
      INNER JOIN git_commit
      ON review.review_url = git_commit.review_url
      INNER JOIN commit_people
      ON commit_people.git_commit_hash = git_commit.hash
      LEFT JOIN (
        SELECT review_url, COUNT(*)
        AS c
        FROM review_people
        WHERE type = 'lgtm'
        GROUP BY review_url) lgtm_count
      ON review.review_url = lgtm_count.review_url
      WHERE lgtm_count.c = 0 OR lgtm_count.c IS NULL
      AND commit_people.type = '%s'""" % commit_people_type)
  data_all = cc.fetchall()
  formatted_data = []
  for data in data_all:
    subject = data[2]
    formatted_data.append([data[0], data[1].strftime("%Y-%m-%d %H:%M:%S"),
                           subject.replace('-', ' '), data[3], data[4]])
  return sorted(formatted_data, key=lambda x: x[1], reverse=True)