# Development Guide

See [structure.md](structure.md) for the full directory map.

## Installation

Install [bazelisk](https://github.com/bazelbuild/bazelisk) as your `bazel`
binary:

```bash
wget -O ~/tools/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.18.0/bazelisk-linux-amd64
chmod +x ~/tools/bazel
# Add ~/tools to PATH
```

## Build and Test

```bash
bazel build //...                          # build everything
bazel test //...                           # run all tests
bazel test //path/to:target                # run a single test
bazel test //... --test_output=all         # show test output
bazel coverage //... --combined_report=lcov  # generate coverage
```

## Linting and Formatting

```bash
./lint.sh --mode check   # check formatting (CI runs this)
./lint.sh --mode format  # auto-format code
```

## CI

- GitHub Actions: [`.github/workflows/`](.github/workflows/)
- Bazel remote caching via [BuildBuddy](https://app.buildbuddy.io/) (requires
  API key in `user.bazelrc`)
- Disk caching via GitHub's cache action
- Remote caching also available via [nativelink](https://www.nativelink.com/)

## Language FAQs

Each language answers: how to lint/format, build, test, run, add dependencies,
package, and release.

### Bazel

```bash
# Regenerate BUILD files
bazel run //:gazelle

# Completely clean
bazel clean --expunge

# Avoid networked backends / remote caches (helpful on slow networks)
bazel build //... --config local
```

**References:** [Bazel query language](https://bazel.build/query/language),
[bzlmod migration](https://bazel.build/external/migration)

### Python

**Style:** 79-char line length (black + isort via `pyproject.toml`)

```bash
# Create virtualenv with all dependencies
bazel run //:create_venv
```

**Adding / modifying external dependencies:**

1. Update `requirements.in`
2. `bazel run //:requirements.update` — updates `requirements_lock.txt`
3. `bazel run //:gazelle_python_manifest.update` — updates `gazelle_python.yaml`

Tests enforce that both update commands have been run after any change to
`requirements.in`.

**Excluding lines from coverage:** `# pragma: no cover`
([docs](https://coverage.readthedocs.io/en/latest/excluding.html))

### Rust

```bash
# Update cargo dependencies
CARGO_BAZEL_REPIN=1 bazel sync --only=crate_index
```

### C++

**Style:** C++23, clang-format (`.clang-format`)

Use `cc_test` (from `//bzl:cc.bzl`) for all tests — see
[C++ Testing](cpp_testing.md) for details.

```bash
# Run buildozer / buildifier manually
bazel run //tools/buildozer -- <args>
bazel run //tools/buildifier -- <args>
```

**ThreadSanitizer on Ubuntu 24.04:**

```bash
sudo sysctl vm.mmap_rnd_bits=30
```

([reference](https://stackoverflow.com/a/77856955))

### JavaScript / Node

```bash
bazel run -- @pnpm//:pnpm --dir $PWD install --lockfile-only
```

## Inspiration

- [jessecureton/python_bazel_template](https://github.com/jessecureton/python_bazel_template)
