load("@rules_platform//platform_data:defs.bzl", "platform_data")

cc_binary(
    name = "main",
    srcs = ["main.cc"],
)

platform_data(
    name = "main_embedded",
    platform = "@bazel_embedded//platforms:cortex_m0",
    target = ":main",
)

package(default_visibility = ["//visibility:private"])
