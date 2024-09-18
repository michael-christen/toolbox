load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("//bzl:py.bzl", "py_binary")
load("//bzl:py.bzl", "grpc_py_library", "proto_py_library", "py_binary", "py_image", "py_test")

exports_files([
    "pytest_main.py",
])

py_binary(
    name = "pytest_main",
    srcs = ["pytest_main.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//pytest"],
)


proto_compile(
    name = "build_python_compile",
    outputs = [
        # "publish_build_event_pb3_grpc.py",
        "build_events_pb2.py",
        "build_events_pb2.pyi",
        "build_status_pb2.py",
        "build_status_pb2.pyi",
        "publish_build_event_pb2.py",
        "publish_build_event_pb2.pyi",
        "publish_build_event_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "@googleapis//google/devtools/build/v1:build_proto",
    visibility = ["//visibility:public"],
)

# grpc_py_library(
#     name = "build_events_py_library",
#     srcs = ["publish_build_event_pb3_grpc.py"],
# )
