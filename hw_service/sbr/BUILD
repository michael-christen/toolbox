load(
    "@pigweed//pw_protobuf_compiler:pw_proto_library.bzl",
    "nanopb_proto_library",
    "nanopb_rpc_proto_library",
)
load("@rules_python//python:proto.bzl", "py_proto_library")

package(default_visibility = ["//visibility:public"])

cc_library(
    name = "service",
    srcs = ["service.cc"],
    hdrs = ["service.h"],
    deps = [
        ":sbr_nanopb_rpc",
        "@pigweed//pw_log",
        "@pigweed//pw_allocator:allocator",
        "@pigweed//pw_assert:check",
        "@pigweed//pw_async2:dispatcher",
    ],
)

proto_library(
    name = "sbr_proto",
    srcs = ["sbr.proto"],
    deps = [
        "//hw_drivers/lis3mdl:lis3mdl_proto",
        "@pigweed//pw_protobuf:common_proto",
    ],
)

nanopb_proto_library(
    name = "sbr_nanopb",
    deps = [":sbr_proto"],
)

nanopb_rpc_proto_library(
    name = "sbr_nanopb_rpc",
    nanopb_proto_library_deps = [":sbr_nanopb"],
    deps = [":sbr_proto"],
)

py_proto_library(
    name = "sbr_pb2",
    deps = [":sbr_proto"],
)
