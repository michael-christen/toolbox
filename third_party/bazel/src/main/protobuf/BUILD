load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//bzl:py.bzl", "proto_py_library")

package(default_visibility = ["//visibility:private"])

proto_library(
    name = "build_proto",
    srcs = ["build.proto"],
    visibility = ["//visibility:public"],
)

cc_proto_library(
    name = "build_cc_proto",
    deps = [":build_proto"],
    visibility = ["//visibility:public"],
)

proto_compile(
    name = "build_python_compile",
    outputs = [
        "build_pb2.py",
        "build_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "build_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "build_py_library",
    srcs = ["build_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)
