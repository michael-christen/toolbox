#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

bazel run //:create_venv
bazel build //packaging:py_wheel_all.reference
venv/bin/pip install `cat bazel-bin/packaging/py_wheel_all.txt`
