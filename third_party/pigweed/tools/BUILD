# gazelle:map_kind py_binary py_binary @rules_python//python:defs.bzl

load("@rules_python//python:defs.bzl", "py_binary")

package(default_visibility = ["//visibility:public"])

filegroup(
    name = "python_source",
    srcs = glob(["*.py"]) + [
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "console",
    srcs = ["console.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//examples/pigweed/modules/blinky:blinky_pb2",
        "//hw_services/sbr:sbr_py_library",
        "@pigweed//pw_system/py:pw_system_lib",
    ],
)
