# Repository Structure

## Overview

All project code lives under the `tlbox/` top-level directory. This is a
language-agnostic namespace — Python, C++, Rust, hardware, and documentation
all coexist under it. The namespace doubles as the Python package name and is
reserved on PyPI, BCR, and npm for future publishing.

Build infrastructure, platform definitions, and vendored dependencies live
outside `tlbox/` at the repo root.

## Directory Map

```
tlbox/                  # all project code
  algorithms/           # standalone algorithm implementations
  apps/                 # runnable applications and CLI tools
    bazel_parser/
    code_metrics/
    ...
  hw/                   # hardware-adjacent code
    drivers/            # C++ hardware drivers
    services/           # C++ hardware services / RPC
    ee/                 # electronics schematics (KiCad)
  notebooks/            # Jupyter notebooks
  ansible_playbooks/    # system configuration and provisioning
  scripts/              # one-off scripts
  testing/              # shared C++ test infrastructure (Catch2)
  utils/                # shared libraries and utilities (Python + C++)
bzl/                    # custom Bazel rules
tools/                  # build tooling (formatters, linters, Bazel wrappers)
platforms/              # Bazel platform and toolchain definitions
third_party/            # vendored dependencies
examples/               # reference implementations and demos
nobazel/                # experiments outside the build system
docs/                   # documentation (this site)
```

## Rules of Thumb

**Where does new code go?**

| What you're adding | Where |
|---|---|
| A new runnable tool or CLI app | `tlbox/apps/<name>/` |
| A reusable library (any language) | `tlbox/utils/` or a new domain subdir |
| Hardware driver or service | `tlbox/hw/drivers/` or `tlbox/hw/services/` |
| Electronics schematic | `tlbox/hw/ee/` |
| A notebook | `tlbox/notebooks/` |
| A one-off script | `tlbox/scripts/` |
| A formatter, linter, or Bazel wrapper | `tools/` |
| A custom Bazel rule or macro | `bzl/` |
| A vendored external dependency | `third_party/` |
| A reference implementation or demo | `examples/` |

**When to create a new subdirectory under `tlbox/`**: when you have a clearly
distinct domain that doesn't fit an existing category. Three related modules
sharing a domain is a reasonable threshold.

**Language is not a directory boundary.** C++, Python, and Rust for the same
domain live together. A hardware driver's `.cc`, `.h`, `.py` bindings, and
`.proto` definitions all belong in `tlbox/hw/drivers/<name>/`.

## The `tlbox/` Namespace

### Python

`tlbox` is a [namespace package](https://peps.python.org/pep-0420/) — no
`__init__.py` files are needed. Python 3 resolves the namespace implicitly.

Imports use the full `tlbox.*` path:

```python
from tlbox.utils.graph_algorithms import weighted_sample
from tlbox.apps.bazel_parser.parsing import parse_build_graph
```

Bazel manages `PYTHONPATH` hermetically via `imports` attributes on
`py_library` targets — no manual path manipulation needed.

### Why not `src/`?

`src/` is a Python packaging convention that prevents accidental imports when
running Python directly from the repo root. In a Bazel repo, imports are
managed hermetically, so `src/` adds label verbosity (`//src/tlbox/...`)
with no benefit.

### Name selection

Several names were evaluated against PyPI, BCR, and npm before settling on
`tlbox`:

| Name | PyPI | Notes |
|---|---|---|
| `tbx` | taken | |
| `tbox` | taken | |
| `tlbx` | taken | |
| `toolbox` | taken | |
| `tlbox` | **free** | chosen |

`tlbox` is also free on BCR and npm.

## What Stays Outside `tlbox/`

| Directory | Reason |
|---|---|
| `bzl/` | Bazel rules are build infrastructure, not project code |
| `tools/` | Formatters, linters, Bazel wrappers — build tooling only |
| `platforms/` | Bazel platform constraints and toolchain configs |
| `third_party/` | Vendored deps — conventional top-level location |
| `examples/` | Demos are not library code; kept separate to avoid noise in API docs |
| `nobazel/` | Explicitly outside the build system |
