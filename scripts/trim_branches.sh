#! /bin/bash

# Trim stale git branches:
#   1. Delete local/remote branches whose PR is closed
#   2. Show remaining unmerged branches for manual review

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)"
cd "${REPO_ROOT}"

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# ── helpers ──────────────────────────────────────────────────────────────────

confirm() {
    local prompt="$1"
    read -r -p "${prompt} [y/N] " answer
    [[ "${answer,,}" == "y" ]]
}

# ── step 1: collect closed-PR branch names ───────────────────────────────────

echo "Fetching closed PRs from GitHub..."
CLOSED_BRANCHES=$(gh pr list --state closed --limit 500 --json headRefName \
    --template '{{range .}}{{.headRefName}}{{"\n"}}{{end}}' | sort -u)

# ── step 2: identify stale local branches ────────────────────────────────────

LOCAL_STALE=()
while IFS= read -r branch; do
    if echo "${CLOSED_BRANCHES}" | grep -qx "${branch}"; then
        LOCAL_STALE+=("${branch}")
    fi
done < <(git branch --format='%(refname:short)' | grep -v "^${CURRENT_BRANCH}$" | grep -v "^master$")

# ── step 3: identify stale remote branches ───────────────────────────────────

echo "Fetching remote branch list..."
git fetch --prune --quiet

REMOTE_STALE=()
while IFS= read -r remote_ref; do
    branch="${remote_ref#origin/}"
    if echo "${CLOSED_BRANCHES}" | grep -qx "${branch}"; then
        REMOTE_STALE+=("${branch}")
    fi
done < <(git branch -r --format='%(refname:short)' | grep "^origin/" | grep -v "^origin/HEAD$" | grep -v "^origin/master$")

# ── step 4: report and delete stale branches ─────────────────────────────────

if [[ ${#LOCAL_STALE[@]} -eq 0 && ${#REMOTE_STALE[@]} -eq 0 ]]; then
    echo "No stale branches found."
else
    if [[ ${#LOCAL_STALE[@]} -gt 0 ]]; then
        echo ""
        echo "Local branches from closed PRs:"
        for b in "${LOCAL_STALE[@]}"; do echo "  $b"; done
        if confirm "Delete these local branches?"; then
            for b in "${LOCAL_STALE[@]}"; do
                git branch -D "${b}"
                echo "  Deleted local: ${b}"
            done
        fi
    fi

    if [[ ${#REMOTE_STALE[@]} -gt 0 ]]; then
        echo ""
        echo "Remote branches from closed PRs:"
        for b in "${REMOTE_STALE[@]}"; do echo "  origin/${b}"; done
        if confirm "Delete these remote branches?"; then
            for b in "${REMOTE_STALE[@]}"; do
                if git push origin --delete "${b}" 2>/dev/null; then
                    echo "  Deleted remote: ${b}"
                else
                    echo "  Skipped (already gone?): ${b}"
                fi
            done
        fi
    fi
fi

# ── step 5: show remaining unmerged branches not in any open PR ───────────────

echo ""
echo "Fetching open PRs..."
OPEN_BRANCHES=$(gh pr list --state open --limit 500 --json headRefName \
    --template '{{range .}}{{.headRefName}}{{"\n"}}{{end}}' | sort -u)

REMAINING=()
while IFS= read -r branch; do
    if ! echo "${OPEN_BRANCHES}" | grep -qx "${branch}"; then
        REMAINING+=("${branch}")
    fi
done < <(git branch --format='%(refname:short)' | grep -v "^${CURRENT_BRANCH}$" | grep -v "^master$")

if [[ ${#REMAINING[@]} -eq 0 ]]; then
    echo "No remaining unmerged local branches."
    exit 0
fi

echo ""
echo "Remaining local branches with no open PR (unmerged, not current):"
for b in "${REMAINING[@]}"; do echo "  ${b}"; done

echo ""
echo "For each branch you can: [k]eep, [d]elete, [r]ebase onto master and diff, or [s]kip"

for b in "${REMAINING[@]}"; do
    echo ""
    echo "─── ${b} ───────────────────────────────────────────────────────────"
    git log --oneline master.."${b}" 2>/dev/null | head -5 || true
    read -r -p "  Action for '${b}' [k/d/r/s]? " action
    case "${action,,}" in
        d)
            git branch -D "${b}"
            echo "  Deleted: ${b}"
            ;;
        r)
            echo "  Attempting rebase onto master..."
            TMPBRANCH="trim-review-$(date +%s)"
            git checkout -b "${TMPBRANCH}" "${b}" 2>/dev/null
            if git rebase master; then
                echo "  Diff against master after rebase:"
                git diff master..."${TMPBRANCH}" --stat
            else
                echo "  Rebase had conflicts; aborting."
                git rebase --abort 2>/dev/null || true
            fi
            git checkout "${CURRENT_BRANCH}" 2>/dev/null
            git branch -D "${TMPBRANCH}" 2>/dev/null || true
            read -r -p "  Now delete '${b}' [y/N]? " del
            if [[ "${del,,}" == "y" ]]; then
                git branch -D "${b}"
                echo "  Deleted: ${b}"
            fi
            ;;
        k | s | *)
            echo "  Kept: ${b}"
            ;;
    esac
done

echo ""
echo "Done trimming branches."
