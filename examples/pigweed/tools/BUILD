load("@rules_python//python:defs.bzl", og_py_binary = "py_binary")

og_py_binary(
    name = "console",
    srcs = ["console.py"],
    deps = [
        "//examples/pigweed/modules/blinky:py_pb2",
        "@pigweed//pw_protobuf:common_py_pb2",
        "@pigweed//pw_rpc:echo_py_pb2",
        "@pigweed//pw_system/py:pw_system_lib",
    ],
    visibility = ["//:__subpackages__"],
)

