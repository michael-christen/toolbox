# Issue Management

This document describes how issues and pull requests are organized in this
repository.

## Project Board

All open issues and PRs are tracked in the
[Toolbox: All](https://github.com/users/michael-christen/projects/4) GitHub
project. New issues and PRs should be added to this project when created.
GitHub's project "Auto-add" workflow (under project Settings → Workflows) can
automate this.

## Labels

Labels describe the nature of the work.

| Label | Description |
| --- | --- |
| `bug` | Something is broken and needs fixing |
| `enhancement` | New feature or improvement to existing functionality |
| `infrastructure` | Build tooling, CI, Bazel rules, language runtimes, repo structure |
| `dependencies` | Dependency updates (version bumps, lockfile changes) |
| `documentation` | Documentation additions or fixes |
| `experiment` | Exploratory work; outcome uncertain |
| `decision` | Requires a decision before work can proceed |

Labels can be combined — e.g. `bug` + `infrastructure` for a broken toolchain,
or `infrastructure` + `experiment` for a speculative build system change.

## Milestones

Milestones group related issues by theme. An issue should be assigned to the
most relevant milestone; it is fine to leave an issue without a milestone if it
does not fit any theme.

| Milestone | Scope |
| --- | --- |
| **Build System Health** | Bazel rules, proto generation, module updates, gazelle |
| **Toolchain & CI** | C++ toolchains, Rust toolchain, LLVM, self-hosted runners |
| **Developer Experience** | Linting, formatting, mypy/pyright, bazelrc, renovate |
| **Python Infra** | Python rules, hermetic python, wheel packaging, jupyterlab |
| **Embedded** | Hardware drivers, Pigweed, nanopb, embedded test infrastructure |
| **Coverage & Testing** | Coverage reporting, expect-failure tests, BES backend |
| **Documentation** | Sphinx, autoapi, documentation build improvements |

## Priorities

Priorities are set on the project board using the **Priority** field.

| Priority | Meaning |
| --- | --- |
| **P0** | Broken and blocking — fix before other work |
| **P1** | High value, should be addressed soon |
| **P2** | Worthwhile but not urgent |
| **P3** | Nice to have, low urgency, or waiting on something else |

## Workflow

1. **New issue or PR**: add to the Toolbox: All project, apply at least one
   label, assign a milestone if applicable, and set a priority.
2. **Stale items**: PRs that have been open for a long time without activity
   should either be closed or rebased and completed. Issues that are no longer
   relevant should be closed with a note.
3. **Bugs** default to P0 or P1 depending on severity. Dependency security
   bumps are P1.
4. **Experiments and low-priority enhancements** default to P3 until there is
   active intent to pursue them.
