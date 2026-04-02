You are running the **issue-workflow** — a guided, end-to-end flow for taking a
GitHub issue from selection through landing and context reset. Work through each
stage in order, pausing at the explicit checkpoints listed below.

The target repository is **michael-christen/toolbox**.
The working directory is `/home/user/toolbox`.
The development branch prefix is `claude/`.

---

## Stage 1 — Select an Issue

1. Use `mcp__github__list_issues` to fetch open issues (state: open).
2. Present the list concisely: number, title, labels, assignee.
3. If `$ARGUMENTS` contains an issue number, use that directly; otherwise ask
   the user which issue to work on.
4. Fetch the full issue body with `mcp__github__get_issue` and display a brief
   summary of what needs to be done.

**Checkpoint**: Confirm the selected issue with the user before proceeding.

---

## Stage 2 — Branch and Implement

1. Derive a branch name: `claude/<issue-number>-<short-slug>` (kebab-case, ≤40
   chars total). Example: `claude/42-fix-bazel-cache`.
2. Create and check out the branch:
   ```
   git checkout -b <branch-name>
   ```
3. Read relevant files before making changes — never modify code you haven't
   read.
4. Implement the fix. Follow all conventions in `CLAUDE.md`:
   - Python: 79-char line length, black + isort
   - C++: C++23, clang-format
   - Bazel: buildifier formatting
5. After changes, run the appropriate checks:
   ```
   ./lint.sh --mode check
   bazel test //...          # or a targeted subset if the full suite is slow
   ```
6. Fix any lint/test failures before continuing.

**Checkpoint**: Show the diff (`git diff`) and confirm readiness to commit.

---

## Stage 3 — Commit and Push

1. Stage specific files (avoid `git add -A` if sensitive files might exist).
2. Write a commit message that explains *why*, not just *what*. Format:
   ```
   <short imperative summary>

   Closes #<issue-number>

   https://claude.ai/code/session_013eKgR1WYFB6zvYaCg11DBT
   ```
3. Commit and push:
   ```
   git push -u origin <branch-name>
   ```
   Retry up to 4× with exponential back-off (2 s, 4 s, 8 s, 16 s) on network
   errors.

---

## Stage 4 — Create Pull Request

1. Use `mcp__github__create_pull_request` with:
   - **title**: concise, imperative, ≤70 chars
   - **body** (use the PR template from `.github/pull_request_template.md` as
     a base):
     ```
     ## Summary
     - <bullet points of what changed and why>

     ## Test plan
     - [ ] lint passes
     - [ ] relevant tests pass
     - [ ] <any manual verification steps>

     Closes #<issue-number>

     https://claude.ai/code/session_013eKgR1WYFB6zvYaCg11DBT
     ```
   - **base**: `master`
   - **head**: `<branch-name>`
2. Report the PR URL to the user.

---

## Stage 5 — Initial Self-Review

Perform a thorough self-review of the PR before human reviewers see it:

1. Re-read every changed file.
2. Check for:
   - Security issues (injection, credential leaks, input validation)
   - Missing tests or coverage gaps
   - Unintended side-effects or regressions
   - Code style violations
   - Overly complex logic that could be simplified
3. If issues are found, push a fix commit before requesting review.
4. Comment on the PR (`mcp__github__create_issue_comment`) with a brief
   self-review note summarising what was checked and any known limitations.

**Checkpoint**: Tell the user the PR is ready for review and provide the URL.

---

## Stage 6 — Watch for Feedback (Review Loop)

1. Subscribe to PR activity:
   ```
   subscribe_pr_activity(pr_number=<N>, repo="michael-christen/toolbox")
   ```
2. As `<github-webhook-activity>` events arrive, for each one:
   - **CI failure**: diagnose the failure, push a fix, explain the root cause
     to the user.
   - **Review comment / change request**: understand the intent. If the fix is
     clear and non-controversial, implement it and reply explaining the change.
     If ambiguous, use `AskUserQuestion` to clarify before acting.
   - **Approval**: proceed to Stage 7.
   - **Duplicate / informational**: acknowledge and skip.
3. After each round of fixes, push to the same branch (no force-push unless
   explicitly requested). Re-request review when ready.

Repeat until the PR receives the required approvals.

---

## Stage 7 — Land the PR

**Checkpoint**: Confirm with the user before merging.

1. Merge using `mcp__github__merge_pull_request` (squash or merge commit per
   user preference; default: squash).
2. Delete the remote branch:
   ```
   git push origin --delete <branch-name>
   ```
3. Delete the local branch:
   ```
   git checkout master && git pull origin master
   git branch -d <branch-name>
   ```
4. Confirm the issue is closed (GitHub auto-closes it via `Closes #N`).

---

## Stage 8 — Clear Context

Tell the user:

> "Issue #N is landed. Run `/clear` to reset the session context for the next
> task."

Then stop — do not start any new work.

---

## General Rules

- Never push to `master` directly.
- Never skip lint or tests.
- Never amend a published commit — always create a new one.
- Never force-push unless the user explicitly requests it.
- Keep commits focused: one logical change per commit.
- If any stage produces an unexpected error, diagnose before retrying.
