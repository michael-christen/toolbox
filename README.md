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

- docs: various writings and documentation of the repo and tools used
- tools: directory of various tools
- experiments: miscellaneous experiments I'm trying out

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

- [ ] decide on rough rules for directory structure, likely don't separate by
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

Testing utilizes [catch2](https://github.com/catchorg/Catch2)

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
