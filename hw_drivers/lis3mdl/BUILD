load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@com_google_emboss//:build_defs.bzl", "emboss_cc_library")
load("@pigweed//pw_build:pigweed.bzl", "pw_cc_test")
load(
    "@pigweed//pw_protobuf_compiler:pw_proto_library.bzl",
    "nanopb_proto_library",
    "nanopb_rpc_proto_library",
)
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//bzl:cc.bzl", "cc_library", "cc_test")
load("//bzl:py.bzl", "proto_py_library")

package(default_visibility = ["//visibility:private"])

emboss_cc_library(
    name = "lis3mdl_emb",
    srcs = ["lis3mdl.emb"],
    visibility = [
        "//hw_service/sbr:__subpackages__",
    ],
)

cc_library(
    name = "lis3mdl",
    srcs = ["lis3mdl.cc"],
    hdrs = ["lis3mdl.h"],
    visibility = [
        "//hw_service/sbr:__subpackages__",
    ],
    deps = [
        ":lis3mdl_emb",
        ":lis3mdl_nanopb",
        "@pigweed//pw_i2c:register_device",
    ],
)

pw_cc_test(
    name = "lis3mdl_pw_test",
    srcs = ["lis3mdl_pw_test.cc"],
    deps = [
        ":lis3mdl",
        ":lis3mdl_emb",
        ":lis3mdl_nanopb",
        "@pigweed//pw_bytes",
        "@pigweed//pw_i2c:address",
        "@pigweed//pw_i2c:device",
        "@pigweed//pw_i2c:initiator_mock",
        "@pigweed//pw_i2c:register_device",
        "@pigweed//pw_result",
        "@pigweed//pw_unit_test",
    ],
)

cc_test(
    name = "lis3mdl_test",
    srcs = ["lis3mdl_test.cc"],
    deps = [
        ":lis3mdl",
        ":lis3mdl_emb",
        ":lis3mdl_nanopb",
        "//testing:catch_main",
        "@pigweed//pw_bytes",
        "@pigweed//pw_i2c:address",
        "@pigweed//pw_i2c:initiator_mock",
        "@pigweed//pw_result",
    ],
)

proto_library(
    name = "lis3mdl_proto",
    srcs = ["lis3mdl.proto"],
    visibility = ["//visibility:public"],
)

# XXX: Unclear how to use these vs. the C++ generated code?
nanopb_proto_library(
    # XXX: Should change to use different suffixes
    name = "lis3mdl_nanopb",
    deps = [":lis3mdl_proto"],
)

nanopb_rpc_proto_library(
    name = "lis3mdl_nanopb_rpc",
    nanopb_proto_library_deps = [":lis3mdl_nanopb"],
    deps = [":lis3mdl_proto"],
)

proto_cc_library(
    name = "lis3mdl_cc_library",
    srcs = ["lis3mdl.pb.cc"],
    hdrs = ["lis3mdl.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "lis3mdl_cpp_compile",
    outputs = [
        "lis3mdl.pb.cc",
        "lis3mdl.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "lis3mdl_proto",
    visibility = ["//visibility:public"],
)

proto_compile(
    name = "lis3mdl_python_compile",
    outputs = [
        "lis3mdl_pb2.py",
        "lis3mdl_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "lis3mdl_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "lis3mdl_py_library",
    srcs = ["lis3mdl_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)
