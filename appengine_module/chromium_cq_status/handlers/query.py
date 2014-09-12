# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from google.appengine.datastore.datastore_query import Cursor
import webapp2

from appengine_module.chromium_cq_status.model.record import Record
from appengine_module.chromium_cq_status.shared.parsing import (
  parse_cursor,
  parse_url_tags,
  parse_fields,
  parse_key,
  parse_query_count,
  parse_request,
  parse_strings,
  parse_timestamp,
)
from appengine_module.chromium_cq_status.shared.utils import compressed_json_dump  # pylint: disable=C0301

def execute_query(
    key, begin, end, tags, fields, count, cursor): # pragma: no cover
  records = []
  next_cursor = ''
  if key and count > 0:
    record = Record.get_by_id(key)
    if record and (
        (not begin or record.timestamp >= begin) and
        (not end or record.timestamp <= end) and
        set(tags).issubset(record.tags) and
        matches_fields(fields, record)):
      records.append(record)
    more = False
  else:
    more = True
    while more and len(records) < count:
      filters = []
      if begin:
        filters.append(Record.timestamp >= begin)
      if end:
        filters.append(Record.timestamp <= end)
      for tag in tags:
        filters.append(Record.tags == tag)
      query = Record.query().filter(*filters).order(-Record.timestamp)
      page_records, next_cursor, more = query.fetch_page(count - len(records),
          start_cursor=Cursor(urlsafe=next_cursor or cursor))
      next_cursor = next_cursor.urlsafe() if next_cursor else ''
      for record in page_records:
        if matches_fields(fields, record):
          records.append(record)

  return {
    'results': [record.to_dict() for record in records],
    'cursor': next_cursor,
    'more': more,
  }

def matches_fields(fields, record): # pragma: no cover
  for field, value in fields.items():
    if not field in record.fields or record.fields[field] != value:
      return False
  return True

class Query(webapp2.RequestHandler): # pragma: no cover
  def get(self, url_tags): # pylint: disable-msg=W0221
    try:
      data = parse_request(self.request, {
        'begin': parse_timestamp,
        'end': parse_timestamp,
        'key': parse_key,
        'tags': parse_strings,
        'fields': parse_fields,
        'count':  parse_query_count,
        'cursor': parse_cursor,
      })
      data['tags'].extend(parse_url_tags(url_tags))
    except ValueError, e:
      self.response.write(e)
      return

    results = execute_query(**data)
    self.response.headers.add_header("Access-Control-Allow-Origin", "*")
    self.response.headers.add_header('Content-Type', 'application/json')
    compressed_json_dump(results, self.response)
