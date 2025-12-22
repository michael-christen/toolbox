load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load(
    "@pigweed//pw_protobuf_compiler:pw_proto_library.bzl",
    "nanopb_proto_library",
    "nanopb_rpc_proto_library",
)
load("@rules_cc//cc:cc_library.bzl", "cc_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//bzl:py.bzl", "grpc_py_library", "proto_py_library")

package(default_visibility = ["//visibility:private"])

cc_library(
    name = "service",
    srcs = ["service.cc"],
    hdrs = ["service.h"],
    implementation_deps = [
        "//hw_drivers/lis3mdl",
        "//hw_drivers/lis3mdl:lis3mdl_emb",
        "@pigweed//pw_assert:check",
    ],
    visibility = [
        "//apps/sbr:__pkg__",
    ],
    deps = [
        ":sbr_nanopb_rpc",
        "@pigweed//pw_allocator:allocator",
        "@pigweed//pw_assert:check",
        "@pigweed//pw_async2:dispatcher",
        "@pigweed//pw_i2c:register_device",
        "@pigweed//pw_log",
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

grpc_py_library(
    name = "sbr_grpc_py_library",
    srcs = ["sbr_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":sbr_py_library"],
)

proto_compile(
    name = "sbr_python_compile",
    outputs = [
        "sbr_pb2.py",
        "sbr_pb2.pyi",
        "sbr_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "sbr_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "sbr_py_library",
    srcs = ["sbr_pb2.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//hw_drivers/lis3mdl:lis3mdl_py_library",
        "@com_google_protobuf//:protobuf_python",
    ],
)

# TODO(#145)
#
# gazelle:ignore
#
# Ignore the whole file (it keeps trying to make this and I can't get the
# necessary sub-dependency)
# > In file included from .../hw_services/sbr/sbr.pb.cc:4:
# > .../hw_services/sbr/sbr.pb.h:31:10: fatal error:
# >  'pw_protobuf_protos/common.pb.h' file not found
# >   #include "pw_protobuf_protos/common.pb.h"
# proto_cc_library(
#     name = "sbr_cc_library",
#     srcs = ["sbr.pb.cc"],
#     hdrs = ["sbr.pb.h"],
#     visibility = ["//visibility:public"],
#     deps = [
#         "//hw_drivers/lis3mdl:lis3mdl_cc_library",
#         "@com_google_protobuf//:protobuf",
#     ],
# )
#
# proto_compile(
#     name = "sbr_cpp_compile",
#     outputs = [
#         "sbr.grpc.pb.cc",
#         "sbr.grpc.pb.h",
#         "sbr.pb.cc",
#         "sbr.pb.h",
#     ],
#     plugins = [
#         "@build_stack_rules_proto//plugin/builtin:cpp",
#         "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
#     ],
#     proto = "sbr_proto",
#     visibility = ["//visibility:public"],
# )
