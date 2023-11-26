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

## TODO
- [ ] decide on rough rules for directory structure, likely don't separate by
  language
- [ ] handle security issues & re-enable dependabot:
  https://github.com/michael-christen/toolbox/security/dependabot

## Installation Instructions

```
wget -O ~/tools/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.18.0/bazelisk-linux-amd64
chmod +x ~/tools/bazel
~/tools/bazel
# Add to path
```

## Issues

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

#### Notes
- bzlmod is where things will be moving to better share dependency information and use a central regirstry: https://bazel.build/external/migration

### Rust

#### Command Quick Reference

Copied from "Bazel"
```
# Update cargo dependencies
# https://www.tweag.io/blog/2023-07-27-building-rust-workspace-with-bazel/
CARGO_BAZEL_REPIN=1 bazel sync --only=crate_index
```
