load("@rules_platform//platform_data:defs.bzl", "platform_data")

cc_binary(
    name = "main",
    srcs = ["main.cc"],
)

platform_data(
    name = "main_embedded",
    target = ":main",
    platform = "@bazel_embedded//platforms:cortex_m0",
)
