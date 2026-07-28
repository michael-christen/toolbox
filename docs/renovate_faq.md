# Renovate FAQ

Common problems seen when a Renovate PR goes red in this repo, and how
they've been resolved. For an automated triage flow, see the
`renovate-debug` Claude Code skill
(`.claude/skills/renovate-debug/SKILL.md`), which covers the same ground in a
format meant to be followed step-by-step.

## Why did my `bazel-module` Renovate PR fail with a weird bzlmod/module-graph error?

Most likely a **module extension namespace collision**. Extensions like
`pip = use_extension(...)` are evaluated once across the whole module graph,
so every module's tags (e.g. `pip.parse(hub_name="pip")`) share one flat
namespace. If a dependency declares the same `hub_name` (or similar) we do,
bzlmod fails or silently picks one. This happened when emboss's BCR module
declared its own `pip` hub, colliding with ours ([#436](https://github.com/michael-christen/toolbox/pull/436)) — fixed by
renaming our hub to `toolbox_pip`.

## I patched a dependency with `single_version_override`, but the patch doesn't seem to apply. Why?

bzlmod reads a module's `MODULE.bazel` **twice**: once during graph
discovery (straight from the registry, ignoring overrides) and once during
fetch (where `single_version_override` patches are actually applied). If your
patch changes anything discovery cares about — a `bazel_dep`, an extension
tag call, the module's own declared name/version — discovery already built
the graph without it, and the patch never has a chance to matter.

Fix: use `archive_override` or `git_override` instead, which replace the
entire source before either phase runs. To confirm this is what's happening,
check `MODULE.bazel.lock` for the module's `registryFileHashes` entry — if it
matches the stock (unpatched) registry file, that confirms discovery bypassed
the patch.

## Bazel says `CONTENT_DOES_NOT_MATCH_TARGET` on my patch, but `patch`/`git apply` applies it fine locally. Why?

Bazel doesn't use system `patch` — it has its own, stricter unified-diff
applier. Two known trip-ups:

- Blank context lines in the diff need a literal leading space character.
  Hand-typed patches often omit this; GNU tools tolerate it, Bazel's applier
  doesn't.
- A single patch file touching multiple unrelated files can fail even when
  each hunk is individually well-formed. Splitting it into one patch file per
  target file (multiple entries in `patches = [...]`) has reliably fixed this
  in practice, even though the root cause isn't fully understood.

## Renovate keeps re-bumping a `git_override` commit I deliberately fixed. How do I stop that?

Renovate's `bazel-module` manager tracks `git_override`/`archive_override`
commits like any other dependency version, and will bump a manually-vetted
pin to whatever the tracked remote's branch tip is — unvalidated. This broke
[#395](https://github.com/michael-christen/toolbox/pull/395) twice: once on
the original bad bump, and again when Renovate silently re-bumped the fork
pin we'd just fixed.

Fix: add a `packageRules` entry in `.github/renovate.json` disabling tracking
for that package, with a `description` explaining why it's pinned:

```json
{
  "matchManagers": ["bazel-module"],
  "matchPackageNames": ["pico-sdk"],
  "description": ["..."],
  "enabled": false
}
```

See [#439](https://github.com/michael-christen/toolbox/pull/439) for the
worked example.

## A pip dependency bump broke the lockfile even though the PR looked fine. Why?

`hashin` (which Renovate uses under the hood for `pip_requirements`) patches
one package's pin without checking whether a *sibling* package requires it at
a specific version. Two cases seen so far:

- `pydantic-core` is always exact-pinned by whichever `pydantic` release is
  installed (`Requires-Dist: pydantic-core==...`) — a standalone bump is
  never valid on its own.
- `docutils` is capped by `sphinx`, `myst-parser`, and `sphinx-rtd-theme`
  simultaneously; a bump past their shared ceiling breaks the build even
  though nothing else in the diff looks wrong.

Both are handled in `.github/renovate.json` — `pydantic-core` is disabled
entirely (it should only ever move as a side effect of a `pydantic` bump, via
a full recompile), `docutils` is capped with `allowedVersions` documenting the
exact sibling constraints. See [#424](https://github.com/michael-christen/toolbox/issues/424) and
[#426](https://github.com/michael-christen/toolbox/pull/426).

Related: a same-day PyPI release once shipped a bad sha256 that `hashin`
fetched before it stabilized, breaking the lockfile ([#435](https://github.com/michael-christen/toolbox/pull/435)). A global
`minimumReleaseAge: 3 days` (with security updates exempted) now gives
releases a short soak period before Renovate picks them up.

## Where do I look before assuming a Renovate failure is new?

- `.github/renovate.json` — most hard-won rules carry a `description` field
  explaining exactly why they exist; read it before re-deriving the same
  conclusion.
- Open tracking issues: [#236](https://github.com/michael-christen/toolbox/issues/236)
  (umbrella bazel-module-updates issue), [#412](https://github.com/michael-christen/toolbox/issues/412)
  (postUpgradeTasks can't handle a brand-new transitive dependency),
  [#413](https://github.com/michael-christen/toolbox/issues/413) (postUpgradeTasks lacks BuildBuddy
  credentials), [#414](https://github.com/michael-christen/toolbox/issues/414) (grpc/googleapis
  `switched_rules` skew, patched but not fixed upstream), [#434](https://github.com/michael-christen/toolbox/issues/434)
  (C++ coverage instrumentation gap in the Pigweed toolchain).
- Worked examples: [#395](https://github.com/michael-christen/toolbox/pull/395),
  [#402](https://github.com/michael-christen/toolbox/pull/402),
  [#431](https://github.com/michael-christen/toolbox/pull/431),
  [#436](https://github.com/michael-christen/toolbox/pull/436),
  [#437](https://github.com/michael-christen/toolbox/pull/437),
  [#439](https://github.com/michael-christen/toolbox/pull/439).

## Decision guide: cap, patch, override, or disable tracking?

In order of preference:

1. **Fix/patch the root cause** when it's a small, genuine upstream bug.
2. **Override to a fork or specific commit** (`archive_override`/`git_override`)
   when upstream/BCR hasn't shipped a fix yet — leave a comment in
   `MODULE.bazel` explaining what it fixes and when it can be reverted.
3. **Cap a version range** only for a real, currently unresolvable
   incompatibility, with a `description` citing the specific conflict.
4. **Disable tracking** only for a deliberately pinned override, or a
   genuinely unfixable case.

Whichever you choose, add a `description` to the `packageRules` entry. It's
the cheapest, most durable form of institutional memory this repo has for
Renovate behavior.
