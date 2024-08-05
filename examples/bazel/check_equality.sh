#!/bin/bash

script=$1
expected=$2

# NOTE: should use location, but can't add as attribute of platform_data,
# and args is overriden by platform_data
actual=$($script examples/bazel/bin1)

echo "ACTUAL: $actual"
echo "EXPECTED: $expected"

if [[ "$expected" == "$actual" ]]; then
  exit 0
else
  exit 1
fi
