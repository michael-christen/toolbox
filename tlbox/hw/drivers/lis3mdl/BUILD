load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("@com_google_emboss//:build_defs.bzl", "emboss_cc_library")
load("@com_google_protobuf//bazel:cc_proto_library.bzl", "cc_proto_library")
load(
    "@pigweed//pw_protobuf_compiler:pw_proto_library.bzl",
    "nanopb_proto_library",
    "nanopb_rpc_proto_library",
)
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//bzl:cc.bzl", "cc_library", "pw_cc_test")
load("//bzl:py.bzl", "proto_py_library")

# gazelle:map_kind cc_test pw_cc_test //bzl:cc.bzl
package(default_visibility = ["//visibility:private"])

# lis3mdl.pb.h is nanopb-generated (C structs); map to nanopb target not cc_proto_library
# gazelle:resolve cc tlbox/hw/drivers/lis3mdl/lis3mdl.pb.h //tlbox/hw/drivers/lis3mdl:lis3mdl_nanopb

emboss_cc_library(
    name = "lis3mdl_emb",
    srcs = ["lis3mdl.emb"],
    # TODO(#144): Required for cross-compilation, investigate more
    enable_enum_traits = False,
    visibility = [
        "//tlbox/hw/services/sbr:__subpackages__",
    ],
)

cc_library(
    name = "lis3mdl",
    srcs = ["lis3mdl.cc"],
    hdrs = ["lis3mdl.h"],
    visibility = [
        "//tlbox/apps/sbr:__subpackages__",
        "//tlbox/hw/services/sbr:__subpackages__",
    ],
    deps = [
        "//tlbox/hw/drivers/lis3mdl:lis3mdl_emb",
        "//tlbox/hw/drivers/lis3mdl:lis3mdl_nanopb",
        "@pigweed//pw_i2c:address",
        "@pigweed//pw_i2c:register_device",
    ],
)

pw_cc_test(
    name = "lis3mdl_pw_test",
    srcs = ["lis3mdl_pw_test.cc"],
    deps = [
        ":lis3mdl",
        "//tlbox/hw/drivers/lis3mdl:lis3mdl_emb",
        "//tlbox/hw/drivers/lis3mdl:lis3mdl_nanopb",
        "@pigweed//pw_bytes",
        "@pigweed//pw_bytes:bit",
        "@pigweed//pw_i2c:address",
        "@pigweed//pw_i2c:initiator_mock",
        "@pigweed//pw_i2c:register_device",
        "@pigweed//pw_log",
        "@pigweed//pw_result",
        "@pigweed//pw_unit_test",
    ],
)

proto_library(
    name = "lis3mdl_proto",
    srcs = ["lis3mdl.proto"],
    visibility = ["//visibility:public"],
)

nanopb_proto_library(
    # TODO(#145): Should change to use different suffixes
    name = "lis3mdl_nanopb",
    deps = [":lis3mdl_proto"],
)

nanopb_rpc_proto_library(
    name = "lis3mdl_nanopb_rpc",
    nanopb_proto_library_deps = [":lis3mdl_nanopb"],
    deps = [":lis3mdl_proto"],
)

cc_proto_library(
    name = "lis3mdl_cc_proto",
    visibility = ["//visibility:public"],
    deps = [":lis3mdl_proto"],
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
