#!/usr/bin/env bash
# Computes Bazel stamp variables for versioning.
# Output is consumed by py_wheel and other stamp-aware rules when --stamp is passed.
set -euo pipefail

COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null || echo "0")

if TAG=$(git describe --exact-match --tags HEAD 2>/dev/null); then
    # On an exact tag — use it as the release version (strip leading 'v')
    GIT_VERSION="${TAG#v}"
else
    # Development build — monotonically increasing, never conflicts with a real release
    GIT_VERSION="0.0.${COMMIT_COUNT}"
fi

echo "STABLE_GIT_VERSION ${GIT_VERSION}"
