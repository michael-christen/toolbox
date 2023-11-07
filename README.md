# toolbox

My personal monorepo.

This will include everything from one-off scripts and experiments to libraries
and applications. I'll likely mostly use Python, C++, and Rust (fingers
crossed) and tie it all into 1 build tool to bring them all together.

This should act as a repository of projects I'm working on and an example of my
latest insights into best practices, design principles, dev-ops usage, etc.

## Layout

- tools: directory of various tools
- experiments: miscellaneous experiments I'm trying out

## To Do

- add tests
- grpc
- gitignore
- config generation / management
- pyright, etc.
- gh tools
- rust all_crate_deps not working
  - could python and cpp do something similar?
- handle security issues & re-enable dependabot:
  https://github.com/michael-christen/toolbox/security/dependabot
- hermetic tools
- github workflow
- using gazelle
  - commented out in workspace, not used yet
- dotconfig
- ssh agent and commit signing
- configure caching
- show it all
  - rust
  - nanopb
  - embedded
  - javascript
  - fast api
  - django
- how to include third party code, etc.
  - https://bazel.build/external/overview#bzlmod seems interesting
- code format: clang-format, yapf, etc.
- XXX checks
- build install with docker, puppet, ansible or something
- testing
- serialization in general
- libraries
  - bit manipulation
- projects
  - embedded
    - C++
    - Rust
    - RTOS build
  - tools
    - stats tracking
- libraries like absl
- python protos, do we need .py and .pyi?
- github squash strategy
- decide on rough rules for directory structure, likely don't separate by
  language
- code gen tools
- setup [buildifier](https://github.com/bazelbuild/buildtools/blob/master/buildifier/README.md)
- python dev workflow with bazel only, eg) ipython equivalent?
- multiple python build types
- release generation
- deployment
- register specific toolchains / lock em down
- different dependency chains
- document common uses of the build system
- how do we share rust around / have separate packages, but shared dependecies?
  - crate_universe, should we only have 1 lock file then?
- py03 for building python?
- mix c++ and rust
- https://docs.platformio.org/ play with / utilize bazel rules
- make my own custom bazel "workspace?" for new rules
- lots of good documentation

### Personal
- switch to ubuntu
- get tmux copy/paste working
- tmux use previous directory
- vim settings
  - std::cout "no member named 'cout' in namespace 'std'"
  - python setup
- bazel completion
- personal jira

## Notes

Bazel:
- use via bazelisk, keeps up to date
- [cpp](https://bazel.build/start/cpp)
  - put in experiments/cpp/hello
- proto
  - example: https://github.com/cgrushko/proto_library
- python: https://github.com/bazelbuild/rules_python/tree/main/examples
- rust: https://github.com/bazelbuild/rules_rust/tree/main/examples
  - https://www.tweag.io/blog/2023-07-27-building-rust-workspace-with-bazel/
  - `CARGO_BAZEL_REPIN=1 bazel sync --only=crate_index`
    - need to run this whenever updating dependencies

## Installation Instructions

```
wget -O ~/tools/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.18.0/bazelisk-linux-amd64
chmod +x ~/tools/bazel
~/tools/bazel
# Add to path
```

## Cross-referenced
- how to reproducibly install bazelisk, download and use

## Issues:

```
INFO: From Compiling src/google/protobuf/generated_message_tctable_lite.cc [for tool]:
In file included from bazel-out/k8-opt-exec-2B5CBBC6/bin/external/com_google_protobuf/src/google/protobuf/_virtual_includes/protobuf_lite/google/protobuf/generated_message_tctable_decl.h:45:0,
from external/com_google_protobuf/src/google/protobuf/generated_message_tctable_lite.cc:42:
bazel-out/k8-opt-exec-2B5CBBC6/bin/external/com_google_protobuf/src/google/protobuf/_virtual_includes/protobuf_lite/google/protobuf/parse_context.h:1147:1: warning: always_inline function might not be inlinable [
-Wattributes]
ParseContext::ParseLengthDelimitedInlined(const char* ptr, const Func& func) {
^~~~~~~~~~~~
external/com_google_protobuf/src/google/protobuf/generated_message_tctable_lite.cc:867:36: warning: always_inline function might not be inlinable [-Wattributes]
PROTOBUF_ALWAYS_INLINE const char* TcParser::FastVarintS1(
^~~~~~~~
external/com_google_protobuf/src/google/protobuf/generated_message_tctable_lite.cc:867:36: warning: always_inline function might not be inlinable [-Wattributes]
```
- externla/com_google_protobuf warning directory does not exist

