---
name: renovate-debug
description: Triage and fix a failing or broken Renovate PR in the michael-christen/toolbox repo — bazel-module bumps that break the Bazel build, pip_requirements bumps that break the lockfile, or Renovate re-bumping a pin it shouldn't touch. Use this whenever a Renovate PR shows red CI, whenever MODULE.bazel.lock or requirements_lock.txt won't regenerate cleanly after a dependency bump, or whenever asked "why did this Renovate PR fail" / "Renovate broke the build" / "why isn't bazel mod deps working". Also use when writing or editing packageRules in .github/renovate.json, to keep the file's self-documentation habit consistent.
---

# Renovate Debug

This repo's Renovate PRs fail in a small number of recurring, non-obvious ways.
Check the failure against the patterns below before treating it as novel —
most Renovate breakage here has already happened once before.

## 1. Identify what's failing

```
gh pr checks <PR#>
```

Note which manager produced the change (visible in the PR title/branch name):
`bazel-module` (`MODULE.bazel`/`MODULE.bazel.lock`), `pip_requirements`
(`requirements.in`/`requirements_lock.txt`), `github-actions`, or
`custom.regex` (the Python toolchain version sync). Then read the actual CI
failure log — the fix depends entirely on which of the patterns below it
matches.

## 2. Known failure patterns

### bazel-module: module graph / bzlmod errors

- **Hub-name collision**: a dependency declares its own tag on a module
  extension we also use (e.g. another module's `pip.parse(hub_name="pip")`
  colliding with ours) — module extensions are evaluated once globally, so
  every module's tags share one flat namespace. Fix the colliding side (rename
  our hub, or patch theirs) rather than capping the dependency forever. See
  `references/bzlmod-gotchas.md` for the full mechanism and worked example
  (#436).
- **A patch via `single_version_override` seems to not apply**: bzlmod's
  module-tag *discovery* phase reads the registry's `MODULE.bazel` directly,
  bypassing `single_version_override` patches entirely. Switch to
  `archive_override` or `git_override`, which fully replace the discovery
  source. Verify the collision by checking `MODULE.bazel.lock`'s
  `registryFileHashes` for a fetch of the *unpatched* registry file — see
  `references/bzlmod-gotchas.md`.
- **`CONTENT_DOES_NOT_MATCH_TARGET` when applying a hand-written patch**:
  Bazel's built-in patch applier is stricter than GNU `patch`/`git apply` —
  blank context lines need a literal leading space, and a combined multi-file
  patch can fail even when each hunk is individually correct. See
  `references/bzlmod-gotchas.md` for how to regenerate and split it.
- **Genuine upstream incompatibility** (not one of the above): confirm with
  `bazel mod deps --lockfile_mode=error` and `bazel mod graph`, then decide
  per the checklist in §3.

### bazel-module: Renovate re-bumping a pin it shouldn't touch

Renovate's `bazel-module` manager tracks `git_override`/`archive_override`
commits like any other version and will bump a manually-vetted pin to an
unvalidated upstream tip. If a `git_override` in `MODULE.bazel` is a
deliberate, tested pin (not a routine upgrade target — e.g. a community fork
carrying a hand-picked fix), add a `packageRules` entry in
`.github/renovate.json` disabling it:

```json
{
  "matchManagers": ["bazel-module"],
  "matchPackageNames": ["<module-name>"],
  "description": ["why this is pinned, what it fixes, links to the PRs/issues"],
  "enabled": false
}
```

Worked example: the `pico-sdk` rule in `.github/renovate.json`, added after
PR #395 broke twice — once on the original bad bump, once when Renovate
auto-re-bumped the fork pin — fixed by PR #439.

### pip_requirements: a bump breaks the lockfile even though the PR "looks fine"

`hashin` patches one package's pin without checking sibling packages that
require it at a specific version (e.g. `pydantic-core` is exact-pinned by
whichever `pydantic` is installed; `docutils` is capped by
sphinx/myst-parser/sphinx-rtd-theme). A standalone bump can violate those
constraints even though nothing in the diff looks wrong. Disable or cap the
dependent package via `packageRules` (see the `pydantic-core`/`docutils`
entries already in `.github/renovate.json` for the pattern and citation
style) and let the full `bazel run //:requirements.update` recompile resolve
it correctly instead.

Related: `minimumReleaseAge: 3 days` is set globally (with
`vulnerabilityAlerts` exempted) after a same-day PyPI release shipped a bad
sha256 that broke the lockfile (#435) — a short soak period is cheaper than
debugging bad hashes after the fact.

## 3. Decision checklist: cap vs. patch vs. override vs. disable-tracking

In order of preference, matching this repo's established practice:

1. **Fix/patch the root cause** if it's a genuine, small upstream bug
   (macro-guard patch, dead `use_repo` call, etc.) — prefer this over
   suppressing the symptom.
2. **`archive_override`/`git_override` to a fork or specific commit** if
   upstream/BCR hasn't shipped a fix yet, with a comment in `MODULE.bazel`
   explaining what it fixes and when to revert.
3. **Cap a version range** (`allowedVersions`) only when a real, currently
   unresolvable incompatibility exists — always with a `description` citing
   the specific conflicting constraint (see the `docutils` rule).
4. **Disable tracking entirely** (`enabled: false`) only for a deliberately
   pinned override that Renovate has no business touching (the `pico-sdk`
   pattern), or a genuinely unfixable case (`pydantic-core`).

Whichever you pick, **add or update a `description` field** on the
`packageRules` entry explaining why — this file is the durable record; PR
descriptions and conversations are not.

## 4. Related docs and issues

- Human-readable FAQ with the same patterns, framed as Q&A:
  `docs/renovate_faq.md`.
- Open threads worth checking before assuming something is new: #236
  (umbrella bazel-module-updates tracking issue), #412 (postUpgradeTasks can't
  handle a brand-new transitive dep), #413 (postUpgradeTasks lacks BuildBuddy
  credentials), #414 (grpc/googleapis `switched_rules` skew — patched, not
  fixed), #434 (C++ coverage instrumentation gap in the Pigweed toolchain).
- Worked examples to reference directly: #395, #402, #431, #436, #437, #438,
  #439.
