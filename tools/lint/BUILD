load("@bazel_skylib//rules:native_binary.bzl", "native_binary")

package(default_visibility = ["//visibility:private"])

native_binary(
    name = "clang_tidy",
    src = "@llvm_toolchain_llvm//:bin/clang-tidy",
    out = "clang_tidy",
)
