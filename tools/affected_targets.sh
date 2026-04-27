#!/usr/bin/env bash
# Identify bazel test (and optionally build) targets affected by changed files.
#
# Approach from https://github.com/bazelbuild/bazel/blob/master/scripts/ci/ci.sh
# adapted with a fallback for files that Bazel can't query directly (MODULE.bazel,
# .bazelrc, *.bzl, etc.) which would otherwise produce a silent false-negative.
#
# Usage:
#   ./tools/affected_targets.sh [--kind <kind>] [--commit-range <range>]
#
#   --kind         bazel kind pattern to filter targets (default: "test")
#                  Use ".*_binary" for binaries, or ".*" for everything.
#   --commit-range git range like "abc123..HEAD" (default: merge-base of origin HEAD)
#
# Output:
#   Newline-separated list of affected targets, or the literal string "//..."
#   if a global file changed and we must fall back to building everything.
#   Prints nothing if no targets are affected.

set -euo pipefail

KIND="test"
COMMIT_RANGE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --kind) KIND="$2"; shift 2 ;;
    --commit-range) COMMIT_RANGE="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

cd "$(git rev-parse --show-toplevel)"

if [[ -z "$COMMIT_RANGE" ]]; then
  MAIN_BRANCH=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null || echo "origin/master")
  COMMIT_RANGE="$(git merge-base "$MAIN_BRANCH" HEAD).."
fi

# Files that affect the entire build graph — Bazel can't query them as source
# targets, so any change to them requires falling back to //...
GLOBAL_PATTERNS=(
  'MODULE\.bazel'
  'MODULE\.bazel\.lock'
  'WORKSPACE'
  'WORKSPACE\.bazel'
  '\.bazelrc'
  '\.bazelversion'
  '.*\.bzl'
)

changed_files=$(git diff --name-only "$COMMIT_RANGE")

if [[ -z "$changed_files" ]]; then
  # No changes at all
  exit 0
fi

for file in $changed_files; do
  for pattern in "${GLOBAL_PATTERNS[@]}"; do
    if [[ "$file" =~ $pattern ]]; then
      echo "//..."
      exit 0
    fi
  done
done

# Resolve each changed file to a Bazel target label
targets=()
for file in $changed_files; do
  label=$(bazel query "$file" 2>/dev/null || true)
  if [[ -n "$label" ]]; then
    targets+=("$label")
  fi
done

if [[ ${#targets[@]} -eq 0 ]]; then
  # All changed files are outside Bazel's graph (e.g. docs, kicad, markdown)
  exit 0
fi

set_expr="set(${targets[*]})"

bazel query \
  --keep_going \
  --noshow_progress \
  "kind(\"${KIND}\", rdeps(//..., ${set_expr})) except attr('tags', 'manual', //...)" \
  2>/dev/null || true
