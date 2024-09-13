# gazelle:map_kind py_binary py_binary @rules_python//python:defs.bzl

load("@rules_python//python:defs.bzl", "py_binary")

package(default_visibility = ["//visibility:public"])

py_binary(
    name = "console",
    srcs = ["console.py"],
    # TODO(#111): pigweed isn't setup for use with mypy yet
    # tags = ["no-mypy"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//examples/pigweed/modules/blinky:blinky_pb2",
        "@pigweed//pw_system/py:pw_system_lib",
    ],
)
