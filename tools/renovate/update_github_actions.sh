#! /bin/bash
#
# Runs Renovate's github-actions manager locally, authenticated as your own
# `gh` account instead of GITHUB_TOKEN.
#
# GITHUB_TOKEN is unconditionally blocked by GitHub from creating/updating
# files under .github/workflows/, regardless of granted permissions (see
# #382, #440, #451) - so CI's Renovate run can never push the
# renovate/github-actions or renovate/major-github-actions branches. A
# personal push has no such restriction, so this scopes a Renovate run to
# just that one manager and pushes as you. Renovate still opens/updates the
# PR itself, same as CI does for every other manager.
#
# Requires: gh CLI logged in with the `workflow` scope
# (`gh auth refresh -s workflow` if `gh auth status` doesn't list it) and
# bazel. Runs via //tools/renovate:renovate (hermetic Node from
# aspect_rules_js) rather than system node/npx - the system node on this
# machine is too old (v12) to run modern Renovate.
#
# Usage: tools/renovate/update_github_actions.sh [--dry-run]

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "${REPO_ROOT}"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

if ! gh auth status &>/dev/null; then
  echo "Not logged in to gh. Run 'gh auth login' first." >&2
  exit 1
fi

if ! gh auth status 2>&1 | grep -q "'workflow'"; then
  echo "Your gh token is missing the 'workflow' scope, required to push" >&2
  echo "changes to .github/workflows/. Run:" >&2
  echo "  gh auth refresh -s workflow" >&2
  exit 1
fi

REPOSITORY="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"

export RENOVATE_TOKEN
RENOVATE_TOKEN="$(gh auth token)"
export RENOVATE_PLATFORM=github
export RENOVATE_REPOSITORIES="${REPOSITORY}"
# Scope strictly to github-actions - every other manager already updates
# fine under CI's GITHUB_TOKEN and shouldn't be re-run under a personal
# identity.
export RENOVATE_ENABLED_MANAGERS='["github-actions"]'

if [[ "${DRY_RUN}" == true ]]; then
  export RENOVATE_DRY_RUN=full
fi

bazel run //tools/renovate:renovate
