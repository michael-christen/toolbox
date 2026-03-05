#!/usr/bin/env bash
# collect.sh — collect Bazel analysis data for a single repo.
#
# Usage: ./collect.sh <repo-dir> <output-dir>
#
# Steps:
#   1. bazel query  (in repo-dir)  → <output-dir>/query.pb
#   2. bazel test   (in repo-dir)  → <output-dir>/bep.pb
#   3. git-capture  (toolbox)      → <output-dir>/file_commit.pb
#   4. process      (toolbox)      → <output-dir>/graph.gml, graph.csv

set -euo pipefail

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DAYS_AGO=400
QUERY_TARGET="//..."
TEST_TARGET="//..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLBOX_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <repo-dir> <output-dir>" >&2
    exit 1
fi

REPO_DIR="$(cd "$1" && pwd)"
mkdir -p "$2"
OUTPUT_DIR="$(cd "$2" && pwd)"

QUERY_PB="${OUTPUT_DIR}/query.pb"
BEP_PB="${OUTPUT_DIR}/bep.pb"
FILE_COMMIT_PB="${OUTPUT_DIR}/file_commit.pb"
OUT_GML="${OUTPUT_DIR}/graph.gml"
OUT_CSV="${OUTPUT_DIR}/graph.csv"

echo "==> Collecting data for: ${REPO_DIR}"
echo "    Output:               ${OUTPUT_DIR}"

# ---------------------------------------------------------------------------
# 1. Bazel query
# ---------------------------------------------------------------------------
echo "==> [1/4] bazel query ${QUERY_TARGET}"
(
    cd "${REPO_DIR}"
    bazel query \
        --notool_deps \
        --output proto \
        "${QUERY_TARGET}" \
        > "${QUERY_PB}"
)

# ---------------------------------------------------------------------------
# 2. Bazel test (captures timing data via BEP)
# ---------------------------------------------------------------------------
echo "==> [2/4] bazel test ${TEST_TARGET}"
(
    cd "${REPO_DIR}"
    bazel test \
        "--build_event_binary_file=${BEP_PB}" \
        "${TEST_TARGET}"
)

# ---------------------------------------------------------------------------
# 3. git-capture
# ---------------------------------------------------------------------------
echo "==> [3/4] git-capture (days-ago=${DAYS_AGO})"
(
    cd "${TOOLBOX_DIR}"
    bazel run //apps/bazel_parser --output_groups=-mypy -- \
        git-capture \
        --repo-dir "${REPO_DIR}" \
        --days-ago "${DAYS_AGO}" \
        --file-commit-pb "${FILE_COMMIT_PB}"
)

# ---------------------------------------------------------------------------
# 4. process
# ---------------------------------------------------------------------------
echo "==> [4/4] process"
(
    cd "${TOOLBOX_DIR}"
    bazel run //apps/bazel_parser --output_groups=-mypy -- \
        process \
        --query-pb "${QUERY_PB}" \
        --bep-pb "${BEP_PB}" \
        --file-commit-pb "${FILE_COMMIT_PB}" \
        --out-gml "${OUT_GML}" \
        --out-csv "${OUT_CSV}"
)

echo "==> Done."
echo "    ${OUT_GML}"
echo "    ${OUT_CSV}"
