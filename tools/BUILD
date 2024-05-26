load("//bzl:py.bzl", "py_library")
load("@rules_multirun//:defs.bzl", "command", "multirun")

command(
    name = "black_format",
    command = "//tools/black",
    environment = {"USE_TARGET_FROM_ENV": "true"},
)
# XXX:
# - Add check
# - Ensure we are passing the right arguments in

multirun(
    name = "format",
    commands = [
        "black_format",
    ],
    jobs = 0,  # Set to 0 to run in parallel, defaults to sequential
)

package(default_visibility = ["//visibility:private"])

py_library(
    name = "utils",
    srcs = ["utils.py"],
    visibility = ["//:__subpackages__"],
)

py_library(
    name = "bazel_utils",
    srcs = ["bazel_utils.py"],
    visibility = ["//:__subpackages__"],
    deps = ["//third_party/bazel/src/main/protobuf:build_py_library"],
)
