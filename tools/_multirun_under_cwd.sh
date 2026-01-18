#!/bin/sh
# From: https://blog.aspect.build/run-tools-installed-by-bazel
# Can also use `bazel run //tools:bazel_env` and the provided binaries with
# direnv: https://blog.aspect.build/bazel-devenv
bazel run "@multitool//tools/$( basename $0 ):cwd" -- "$@"
