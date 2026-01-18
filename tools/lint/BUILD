load("@bazel_skylib//rules:native_binary.bzl", "native_binary")

package(default_visibility = ["//visibility:private"])

# Use Pigweed's LLVM toolchain (saves ~6GB vs toolchains_llvm). See #220.
# Note: Using canonical name since Pigweed's llvm_toolchain isn't directly visible.
native_binary(
    name = "clang_tidy",
    src = "@@pigweed++_repo_rules6+llvm_toolchain//:bin/clang-tidy",
    out = "clang_tidy",
)
