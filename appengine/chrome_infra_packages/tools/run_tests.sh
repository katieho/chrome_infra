#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
cd "$DIR/../../"
./test.py test "$DIR" "$@" --html-report "$DIR/.coverage"
