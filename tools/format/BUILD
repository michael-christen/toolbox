load("@aspect_rules_lint//format:defs.bzl", "format_multirun")

package(default_visibility = ["//visibility:private"])

format_multirun(
    name = "format",
    c = "@llvm_toolchain_llvm//:bin/clang-format",
    cc = "@llvm_toolchain_llvm//:bin/clang-format",
    visibility = ["//:__subpackages__"],
)
