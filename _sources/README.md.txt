# toolbox

My personal monorepo.

Find [docs here](https://michael-christen.github.io/toolbox)

This will include everything from one-off scripts and experiments to libraries
and applications. I'll likely mostly use Python, C++, and Rust (fingers crossed)
and tie it all into 1 build tool to bring them all together.

This should act as a repository of projects I'm working on and an example of my
latest insights into best practices, design principles, dev-ops usage, etc.

## Badges

[![codecov](https://codecov.io/gh/michael-christen/toolbox/graph/badge.svg?token=GGS6QHC5YP)](https://codecov.io/gh/michael-christen/toolbox)

NOTE: Our coverage setup doesn't find completely uncovered files. We'll need to
fix that at some point, for now be aware of it.

## Layout

All project code lives under `tlbox/` — a language-agnostic namespace for
Python, C++, Rust, and hardware code alike. See
[docs/structure.md](docs/structure.md) for the full rationale and rules of
thumb.

```
tlbox/             # all project code
  algorithms/      # standalone algorithm implementations
  apps/            # runnable applications (bazel_parser, code_metrics, etc.)
  hw/
    drivers/       # hardware drivers (C++)
    services/      # hardware services (C++)
    ee/            # electronics schematics (KiCad)
  notebooks/       # Jupyter notebooks
  ansible_playbooks/
  scripts/         # one-off scripts
  testing/         # shared C++ test infrastructure (gtest_main, pw_log handler)
  utils/           # shared libraries and utilities
bzl/               # custom Bazel rules
tools/             # build tooling (formatters, linters, Bazel wrappers)
platforms/         # Bazel platform and toolchain definitions
third_party/       # vendored dependencies
examples/          # reference implementations and demos
nobazel/           # experiments outside the build system
docs/              # documentation (Sphinx)
```

## Configuration / Tools Used

This section describes how the various tools are setup and used in the repo.

### Installation Instructions

```
wget -O ~/tools/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.18.0/bazelisk-linux-amd64
chmod +x ~/tools/bazel
~/tools/bazel
# Add to path
```

### Getting Started

## TODO

- [x] decide on rough rules for directory structure, likely don't separate by
      language
- [ ] handle security issues & re-enable dependabot:
      https://github.com/michael-christen/toolbox/security/dependabot
- [ ] Add linter
- [ ] Look into new tools: fd, fzf, zoxide

### CI

- github actions, see [.github/workflows/](.github/workflows/)
- bazel
  - disk caching uses github's cache action
  - remote caching handled externally with
    [nativelink](https://www.nativelink.com/)
    - see
      [dashboard](https://app.nativelink.com/c690e34c-beac-420a-b672-6320b8f5b419/dashboard)
      for more detailed metrics.
  - [buildbuddy](https://app.buildbuddy.io/)

## References

### Bazel

- [query](https://bazel.build/query/language)

#### Command Quick Reference

```
# Completely clean
bazel clean --expunge

# Update cargo dependencies
# https://www.tweag.io/blog/2023-07-27-building-rust-workspace-with-bazel/
CARGO_BAZEL_REPIN=1 bazel sync --only=crate_index
```

NOTE: this doesn't seem to be working ...

#### Notes

- bzlmod is where things will be moving to better share dependency information
  and use a central regirstry: https://bazel.build/external/migration

## Language FAQs

Generally, each language needs a way to answer these questions:

- How to check & enforce style and typing? (linter & formatter)
- How to bulid?
- How to test?
- How to run?
- How to add dependencies?
- How to package?
- How to release / distribute?

### Rust

#### Command Quick Reference

Copied from "Bazel"

```
# Update cargo dependencies
# https://www.tweag.io/blog/2023-07-27-building-rust-workspace-with-bazel/
CARGO_BAZEL_REPIN=1 bazel sync --only=crate_index
```

### Python

#### Excluding coverage

`# pragma: no cover` https://coverage.readthedocs.io/en/latest/excluding.html

#### Adding / Modifying External Dependencies

1. Update `requirements.in`
2. `bazel run //:requirements.update` to modify `requirements_lock.txt`
3. `bazel run //:gazelle_python_manifest.update` to modify `gazelle_python.yaml`

NOTE: Once `requirements.in` is modified, tests will ensure the above commands
have been run (or CI will fail)

### C++

Use `cc_test` (from `//bzl:cc.bzl`) for all tests. It automatically delegates to
`pw_cc_test` when `@pigweed//pw_unit_test` is in `deps`, enabling Pigweed
backends (I2C mocks, async, etc.). Both paths use the
[Google Test](https://google.github.io/googletest/) API (`TEST`, `EXPECT_*`,
`ASSERT_*`). See `docs/cpp_testing.md` for details.

### Miscellaneous

```
bazel run //tools/buildozer -- <args>
bazel run //tools/buildifier -- <args>
bazel run -- @pnpm//:pnpm --dir $PWD install --lockfile-only
```

#### Bazel Options

```
# Avoid networked backends / remote caches, particularly helpful when home
network is slow
--config local
```

#### Get tsan to work on Ubuntu 24.04

https://stackoverflow.com/a/77856955

```
sudo sysctl vm.mmap_rnd_bits=30
```

#### Inspiration

- https://github.com/jessecureton/python_bazel_template
