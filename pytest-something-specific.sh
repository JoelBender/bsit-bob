#!/bin/bash

SCRIPT_NAME=${BASH_SOURCE##*/}
LOG_FILE=${SCRIPT_NAME%.*}.log

uv run pytest -s -v \
    --log-cli-level DEBUG \
    --log-file=$LOG_FILE \
    tests/test__template.py::test_some_function
#   tests/test__template.py::TestCaseTemplate::test_something

