# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Personal monorepo using Bazel as the primary build system. Contains Python, C++, and Rust code with embedded systems support via Pigweed framework. Uses bzlmod for dependency management.

## Essential Commands

### Build and Test
```bash
bazel build //...                    # Build everything
bazel test //...                     # Run all tests
bazel test //path/to:target          # Run single test
bazel test //... --test_output=all   # Show test output
bazel coverage //... --combined_report=lcov  # Generate coverage
```

### Linting and Formatting
```bash
./lint.sh --mode check   # Check formatting (CI runs this)
./lint.sh --mode format  # Auto-format code
```

### Python Dependencies
When adding/modifying Python dependencies:
1. Update `requirements.in`
2. Run `bazel run //:requirements.update` to update `requirements_lock.txt`
3. Run `bazel run //:gazelle_python_manifest.update` to update `gazelle_python.yaml`

### Rust Dependencies
```bash
CARGO_BAZEL_REPIN=1 bazel sync --only=crate_index
```

### BUILD File Generation
```bash
bazel run //:gazelle   # Regenerate BUILD files
```

### Local Development (slow network)
```bash
bazel build //... --config local  # Disables remote cache and BES
```

### Virtual Environment
```bash
bazel run //:create_venv  # Creates venv/ directory with dependencies
```

## Architecture

### Build System
- **Bazel with bzlmod**: Dependencies in `MODULE.bazel`, lockfile in `MODULE.bazel.lock`
- **Custom Python rules**: `//bzl:py.bzl` wraps standard rules to add pytest support and mypy integration
- **Gazelle**: Auto-generates BUILD files for Python and Proto; configured in root BUILD file
- **Mypy**: Enabled by default via `--output_groups=+mypy` in `.bazelrc`

### Key Directories
- `apps/`: Standalone applications (bazel_parser, code_metrics, sbr)
- `examples/`: Reference implementations demonstrating Bazel, Pigweed, Python patterns
- `tools/`: Build tooling (formatters, linters, utilities)
- `bzl/`: Custom Bazel rules including `py.bzl` for Python and `cc.bzl` for C++
- `hw_drivers/`, `hw_services/`: Hardware abstraction layers
- `platforms/`: Platform definitions for cross-compilation
- `third_party/`: Vendored dependencies and proto definitions

### Testing
- Python: Uses pytest via custom `py_test` rule in `//bzl:py.bzl`
- C++: Uses Catch2 framework
- Coverage exclusion: `# pragma: no cover`

### CI/CD
- GitHub Actions workflow in `.github/workflows/build-and-test.yml`
- Remote caching via BuildBuddy (requires API key in `user.bazelrc`)
- Coverage reporting to Codecov

## Code Style
- Python: 79 char line length (black + isort configured in `pyproject.toml`)
- C++: C++23 standard, clang-format configured in `.clang-format`
- Bazel files: buildifier formatting

## Embedded Development (Pigweed)
The repo includes Pigweed integration for embedded targets:
- Platform configs in `platforms/` and `//tools/platforms`
- RP2 (Raspberry Pi Pico) support via pico-sdk
- Custom system backends in `system/`
