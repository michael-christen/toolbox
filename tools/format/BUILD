load("@aspect_rules_lint//format:defs.bzl", "format_multirun")

package(default_visibility = ["//visibility:private"])

# Use Pigweed's LLVM toolchain (saves ~6GB vs toolchains_llvm). See #220.
# Note: Using canonical name since Pigweed's llvm_toolchain isn't directly visible.
format_multirun(
    name = "format",
    c = "@@pigweed++_repo_rules6+llvm_toolchain//:bin/clang-format",
    cc = "@@pigweed++_repo_rules6+llvm_toolchain//:bin/clang-format",
    visibility = ["//:__subpackages__"],
)
