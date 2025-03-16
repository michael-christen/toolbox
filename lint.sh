#! /bin/bash

set -euo pipefail

# Function to print usage
function print_usage {
  echo "Usage: $0 --mode [check|format]"
  exit 1
}

function grep_xxx {
  # Don't show up in the search
  X="X"
  BAD_STRING="$X$X$X"
  # Raise and re-report if found
  if git grep --quiet ${BAD_STRING}; then
    echo "${BAD_STRING} found in source"
    git grep ${BAD_STRING}
    exit 1
  fi
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

# Check if the flag was set
if [ -z "$mode" ]; then
  print_usage
elif [ "$mode" = "check" ]; then
  BUILDIFIER_ARGS=("-lint=off" "-mode=check" "-v=false")
  PRETTIER_ARGS=("--check" "--config ${REPO_ROOT}/.prettierrc")
  BAZEL_TOOL="//tools:check"
  GAZELLE_ARGS=("-mode" "diff")
  RULES_LINT_CMD="//tools/format:format.check"
elif [ "$mode" = "format" ]; then
  BUILDIFIER_ARGS=("-lint=fix" "-mode=fix" "-v=false")
  PRETTIER_ARGS=("--write" "--config ${REPO_ROOT}/.prettierrc")
  BAZEL_TOOL="//tools:format"
  GAZELLE_ARGS=("-mode" "fix")
  RULES_LINT_CMD="//tools/format:format"
fi
PRETTIER_INVOCATION=""


function print_error {
    read line file <<<$(caller)
    printf "\n⛔️ An error occurred during the following lint step ⛔️\n" >&2
    sed "${line}q;d" "$file" >&2
}
trap print_error ERR

CONFIG="--config quiet"
# Can uncomment to get more verbose
# CONFIG=""

# Build for use
bazel build ${CONFIG} --output_groups=-mypy -- //packaging:query_generator

# Run query generator
./bazel-bin/packaging/query_generator --mode $mode

echo $BAZEL_FILES | xargs bazel run ${CONFIG} -- //tools/buildifier ${BUILDIFIER_ARGS[@]}
bazel run ${CONFIG} -- ${BAZEL_TOOL}
echo $MARKDOWN_FILES | xargs bazel run ${CONFIG} -- //tools/prettier ${PRETTIER_ARGS[@]}
bazel run ${CONFIG} -- //:gazelle ${GAZELLE_ARGS[@]}

bazel run $RULES_LINT_CMD

# Add back in when fixed
# grep_xxx

# TODO(#139)
# Add this back in (conflicts with emboss at the moment)
# See https://github.com/aspect-build/rules_lint/blob/main/example/lint.sh
# --aspects=//tools/lint:linters.bzl%clang_tidy


# TODO(#57): Re-enable this check when we fix the false errors
# - name: bzlmod lockfile
#   run: |
#     bazel mod deps --lockfile_mode=error


printf "\n✨ Linting completed successfully! ✨\n"
