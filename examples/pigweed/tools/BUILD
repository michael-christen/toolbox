load("@rules_python//python:defs.bzl", og_py_binary = "py_binary")

og_py_binary(
    name = "console",
    srcs = ["console.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//examples/pigweed/modules/blinky:blinky_pb2",
        "@pigweed//pw_protobuf:common_py_pb2",
        "@pigweed//pw_rpc:echo_py_pb2",
        "@pigweed//pw_system/py:pw_system_lib",
    ],
)

package(default_visibility = ["//visibility:public"])
