load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//bzl:py.bzl", "proto_py_library")

package(default_visibility = ["//visibility:private"])

proto_library(
    name = "build_proto",
    srcs = ["build.proto"],
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "build_cc_library",
    srcs = ["build.pb.cc"],
    hdrs = ["build.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "build_cpp_compile",
    outputs = [
        "build.pb.cc",
        "build.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "build_proto",
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
    # Get .pyi
    data = ["build_pb2.pyi"],
    # Don't run mypy on this itself
    tags = ["no-mypy"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)
