# Bazel Experiment

I'd like to try to setup an embedded toolchain with Bazel. I haven't used Bazel
much before, so I'm planning on:
- Running the tutorial
- Learning more about the internals
- Tweaking some things
- Learning what's necessary for cross compilation
- Reading some others' attempts at cross-compilation:
  https://github.com/prattmic/embedded-bazel
- Giving it a shot myself

## Glossary

| Name | Meaning |
| ---- | ------- |
| Target | binary |
| `WORKSPACE` | Identifies directory and contents as a Bazel workspace |
| `BUILD` | A file that defines how to build parts of the project |
| Package | A directory within the workspace that contains a `BUILD` file |
| toolchain | Supply "Make variables"for target to use in some of its attributes |
| Starlark | Bazel's language, inspired by Python; usually defined in `.bzl` files |

## Location Specification / Target Label

What the heck is `//main:hello-world`?

`//${PATH_TO_PACKAGE}:${TARGET}`

w/in a `BUILD` file you can simply specify `:${TARGET}`.

`//...` describes the entire workspace.

## Descriptions

### `BUILD`

Contains several types of instructions.

Type: `build rule` describes how to build outputs; ie) executable binaries or
libraries. Each build rule is a target; specifies source files and
dependencies, possibly other targets.

Instructions:

#### `cc_binary`

- name
- srcs
- deps
- visibility: example `//test:__pkg__`


## Questions

- How to run `bazel` from outside the workspace?
- How to compile 2 targets with the same dependencies, but different required
  flags, ie) one with cross compiler, one without.
- Link a separate file?
	- Just make a different binary?

## How To

Generate dependency graph:

```
xdot <(bazel query --nohost_deps --noimplicit_deps 'deps(${target})' --output graph)
```

## Cross Compilation Requirements

- Make multiple targets and tests based on:
	- Platform
	- Target
- Use separate compiler if compiling for host. Use `--compiler` and `--cpu`
  options.

## Miscellaneous Notes

- [Bazel C++ Best Practices](https://docs.bazel.build/versions/master/bazel-and-cpp.html)
recommended making many granular `cc_library`s and one `cc_test` per
`cc_library`.
- External Dependencies: reference to external workspaces (on FS or remote)
  with top level BUILD file.
- `cc_toolchain` can be specified by `CcToolchainConfigInfo`
- `genrule` allows you to use Bazel like a Makefile
- Compiling targets for multiple target platforms at the same time
(dynamic configurations) may not have great support right now.

## Embedded / Toolchain Notes

- Could use external dependencies to keep most platform specific code that
  never changes outside of the repo. May not want to do that though.
- `cc_toolchain_suite` in `BUILD` points target using `--crosstool_top`
- `features` define one or more flag groups (list of flags that apply to Bazel
  actions)
- https://docs.bazel.build/versions/master/tutorial/cc-toolchain-config.html

## References

- [Bazel](https://www.bazel.build/)
- [C/C++ Rules](https://docs.bazel.build/versions/master/be/c-cpp.html)
- https://docs.bazel.build/versions/master/be/overview.html
- https://docs.bazel.build/versions/master/build-ref.html
- https://docs.bazel.build/versions/master/user-manual.html
- https://docs.bazel.build/versions/master/tutorial/cc-toolchain-config.html
- https://groups.google.com/forum/#!topic/bazel-discuss/-8T30fYg3UM
- https://github.com/prattmic/embedded-bazel
