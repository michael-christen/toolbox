#!/usr/bin/env bash
#
# Shows an end-to-end workflow for linting without failing the build.
# This is meant to mimic the behavior of the `bazel lint` command that you'd have
# by using the Aspect CLI.
#
# We recommend using Aspect CLI instead!
set -o errexit -o pipefail -o nounset

if [ "$#" -eq 0 ]; then
	echo "usage: lint.sh [target pattern...]"
	exit 1
fi

# Produce report files
# You can add --aspects_parameters=fail_on_violation=true to make this command fail instead.
# TODO: put back ruff after the output paths don't collide
bazel build --aspects //tools:lint.bzl%eslint,//tools:lint.bzl%buf,//tools:lint.bzl%flake8,//tools:lint.bzl%pmd,//tools:lint.bzl%shellcheck --output_groups=rules_lint_report $@

# Show the results.
# `-mtime -1`: only look at files modified in the last day, to mitigate showing stale results of old bazel runs.
# `-size +1c`: don't show files containing zero bytes
for report in $(find $(bazel info bazel-bin) -mtime -1 -size +1c -type f -name "*.aspect_rules_lint.report"); do
	echo "From ${report}:"
	cat "${report}"
	echo
done
