# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

NPM_VERSION := $(shell npm --version 2>/dev/null)
BOWER_VERSION := $(shell bower --version 2>/dev/null)
GIT_REVISION := $(shell git rev-parse --short HEAD)

check:
ifndef NPM_VERSION
	$(error npm not found. Install from nodejs.org or see README)
endif
ifndef BOWER_VERSION
	@echo "bower not found. Installing:";
	npm install -g bower
endif

test: check
	./node_modules/karma/bin/karma start

single-test: check
	./node_modules/karma/bin/karma start --single-run

deploy:
	appcfg.py --oauth2 update app.yaml highend.yaml --version `git rev-parse --short HEAD`

.PHONY: check test single-test
