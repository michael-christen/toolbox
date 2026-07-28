# bzlmod gotchas

Technical detail behind the bazel-module patterns in `SKILL.md`. Read this
when the failure is actually a bzlmod/module-graph problem, not just a plain
version bump.

## Module extensions share one global namespace

A module extension (e.g. `pip = use_extension("@rules_python//python/extensions:pip.bzl", "pip")`)
is evaluated exactly once across the *entire* module graph for a given build —
not once per module. Every module that calls a tag on that extension (e.g.
`pip.parse(hub_name="pip", ...)`) contributes to one shared, flat namespace of
generated repos. If two unrelated modules both pick `hub_name="pip"`, bzlmod
sees two tags trying to define the same repo and fails (or, worse, silently
picks one, producing hard-to-explain missing-package errors).

**Worked example (#436)**: emboss's BCR-published `MODULE.bazel` calls
`pip.parse(hub_name="pip", ...)` for its own Python deps. Once emboss
appeared in our module graph (pulled in via the Pigweed roll), its `pip` hub
collided with the repo's own `pip` hub. Fixed by renaming our hub to
`toolbox_pip` (touches every `@pip//` reference in the repo — a mechanical,
if wide, rename). The alternative — patching *emboss's* `MODULE.bazel` to
rename its hub instead — was tried first via `single_version_override` and
hit the discovery-phase gotcha below, then via `archive_override`, but was
abandoned once it turned out emboss's own subsequent BCR release fixed things
and the rename had already landed.

## `single_version_override` patches don't apply during tag discovery

bzlmod resolves the module graph in roughly two passes:

1. **Discovery**: read every module's `MODULE.bazel` (from the registry, or
   from an override's source) to find `bazel_dep` and extension tag calls,
   and build the full module graph / repo mapping.
2. **Fetch**: actually download and materialize each repo, applying patches
   from overrides at this stage.

`single_version_override`'s `patches` attribute is only consulted at fetch
time — but discovery already read the *unpatched* `MODULE.bazel` straight
from the registry to build the graph. If your patch modifies anything that
discovery cares about (a `bazel_dep`, a module extension tag call, the module
name/version itself), the patch is silently irrelevant: the graph was already
built without it.

`archive_override` and `git_override` don't have this problem because they
replace the *entire source*, including what discovery reads, before either
pass runs.

**How to tell this is happening**: after `bazel mod deps --lockfile_mode=update`,
open `MODULE.bazel.lock` and search for the module's `registryFileHashes`
entry. If it references a hash of the registry's stock `MODULE.bazel` (not a
locally-patched one), discovery bypassed your patch. Switching the override
type resolves it — no other change needed.

## Bazel's built-in patch applier vs. GNU `patch`

Bazel does not shell out to system `patch`; it uses its own Java-based unified
diff applier, which is stricter in two ways that GNU `patch`/`git apply`
tolerate silently:

- **Blank context lines must have a literal leading space.** A hand-typed or
  hand-edited unified diff often has a truly empty line (0 characters) where
  the original file had a blank line in the context region. GNU tools treat
  that as "matches a blank line"; Bazel's patcher does not, and will fail with
  `CONTENT_DOES_NOT_MATCH_TARGET` even though the patch is semantically
  correct. Fix: regenerate the patch with a tool that preserves the space
  (e.g. `diff -u`/`git diff` from an actual working tree edit, rather than
  hand-typing hunks), or explicitly insert a single space character on any
  blank context line.
- **Combined multi-file patches can fail even when individually correct.**
  Empirically, a single `.patch` file touching two unrelated files (e.g. a
  `MODULE.bazel` hunk and a `BUILD` hunk in one diff) has failed
  `CONTENT_DOES_NOT_MATCH_TARGET` where splitting it into two patch files —
  each targeting exactly one file, passed as two entries in `patches = [...]`
  — succeeded immediately with no other change. The root cause isn't fully
  understood; treat "split per file" as the reliable workaround when a
  correctly-formatted combined patch still won't apply.

## Renovate's `bazel-module` manager and `git_override`

Renovate's `bazel-module` manager parses `MODULE.bazel` for version-like
strings, including `git_override(... commit = "...")`. It has no concept of
"this commit was hand-picked and validated" vs. "this is tracking upstream" —
it will happily open a PR (or, worse, silently rebase an existing PR branch)
bumping the commit to whatever the tracked remote's branch tip currently is.

For a routine dependency this is exactly the desired behavior. For a
deliberately pinned fork commit (chosen because it contains a specific,
manually-verified fix and nothing else), it is not — the new tip commit is
unvalidated and may reintroduce the very problem the pin was fixing, or add
unrelated breakage from the fork's own ongoing development.

The fix is not a version cap (`allowedVersions` doesn't meaningfully apply to
a `git_override` commit hash) — it's disabling tracking entirely via
`packageRules` + `matchPackageNames` + `enabled: false`, same as is already
done for other permanently-pinned or permanently-capped dependencies
(`rules_rust`, `pydantic-core`). Revisit / remove the rule once
upstream or BCR ships a real fix and the override itself can be dropped.
