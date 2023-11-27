#!/bin/sh

# Ensure we've been run with `bazel run`
if [ -z "${BUILD_WORKING_DIRECTORY-}" ]; then
	echo "error BUILD_WORKING_DIRECTORY not set"
	exit 1
fi

# Get the fullpath for the executable
cmd="$(realpath ${1})"
# Switch to where bazel was called from
cd "${BUILD_WORKING_DIRECTORY}"
# Remove the non-realpath'd executable from the argument list $@
shift

# Concatenate them together again
exec "${cmd}" "$@"
