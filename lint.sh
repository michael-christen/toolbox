#! /bin/bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)"

# Find all Bazel-ish files - these templates come from Buildifier's default search list
BAZEL_FILES=$(find ${REPO_ROOT} -type f \
            \(   -name "*.bzl" \
              -o -name "*.sky" \
              -o -name "BUILD.bazel" \
              -o -name "BUILD" \
              -o -name "*.BUILD" \
              -o -name "BUILD.*.bazel" \
              -o -name "BUILD.*.oss" \
              -o -name "MODULE.bazel" \
              -o -name "WORKSPACE" \
              -o -name "WORKSPACE.bazel" \
              -o -name "WORKSPACE.oss" \
              -o -name "WORKSPACE.*.bazel" \
              -o -name "WORKSPACE.*.oss" \) \
              -print)

# Find all Markdown-ish files
MARKDOWN_FILES=$(find ${REPO_ROOT} -type f -name "*.md" -print)

# Function to print usage
print_usage() {
  echo "Usage: $0 --mode [check|format]"
  exit 1
}

# Parse arguments using getopt
OPTS=$(getopt -o '' -l 'mode:' -- "$@")
if [ $? != 0 ]; then
  print_usage
fi
eval set -- "$OPTS"

# Initialize the flag
mode=

while true; do
  case "$1" in
    --mode)
      if [ "$2" = "check" ]; then
        mode=$2
      elif [ "$2" = "format" ]; then
        mode=$2
      else
        echo "Invalid value for --mode. Use 'check' or 'format'."
        exit 1
      fi
      shift 2
      ;;
    --)
      shift
      break
      ;;
    *)
      print_usage
      ;;
  esac
done

# Update ARGS based on input
ISORT_ARGS=("${REPO_ROOT}" "--dont-follow-links")
BLACK_ARGS=("${REPO_ROOT}")
FLAKE8_ARGS=("${REPO_ROOT}")

# Check if the flag was set
if [ -z "$mode" ]; then
  print_usage
elif [ "$mode" = "check" ]; then
  # XXX: lint off?
  BUILDIFIER_ARGS=("-lint=off" "-mode=check" "-v=false")
  ISORT_ARGS+=("--check")
  BLACK_ARGS+=("--check")
  # flake8 doesn't format
  PRETTIER_ARGS=("--check" "--config ${REPO_ROOT}/.prettierrc")
  BAZEL_TOOL="//tools:check"
elif [ "$mode" = "format" ]; then
  BUILDIFIER_ARGS=("-lint=fix" "-mode=fix" "-v=false")
  PRETTIER_ARGS=("--write" "--config ${REPO_ROOT}/.prettierrc")
  BAZEL_TOOL="//tools:format"
fi


function print_error {
    read line file <<<$(caller)
    printf "\n⛔️ An error occurred during the following lint step ⛔️\n" >&2
    sed "${line}q;d" "$file" >&2
}
trap print_error ERR

#####################
# Bazel file linting
#####################
BUILDIFIER_INVOCATION="bazel run --config quiet -- //tools/buildifier ${BUILDIFIER_ARGS[@]}"
echo $BAZEL_FILES | xargs ${BUILDIFIER_INVOCATION}


#################
# Python linting
#################
# Sort imports
bazel run --config quiet  -- //tools/isort ${ISORT_ARGS[@]}
# Autoformat
bazel run --config quiet -- //tools/black ${BLACK_ARGS[@]}
# Ensure flake8 compliance
bazel run --config quiet  -- //tools/flake8 ${FLAKE8_ARGS[@]}

# XXX: Replace most with this
# bazel run --config quiet ${BAZEL_TOOL}

#################
# Markdown Linting
#################
PRETTIER_INVOCATION="bazel run --config quiet -- //tools/prettier ${PRETTIER_ARGS[@]}"
echo $MARKDOWN_FILES | xargs ${PRETTIER_INVOCATION}


printf "\n✨ Linting completed successfully! ✨\n"

# Add git grep XXX?
# And --check option
#
