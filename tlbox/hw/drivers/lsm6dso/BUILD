load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("@com_google_emboss//:build_defs.bzl", "emboss_cc_library")
load("@com_google_protobuf//bazel:cc_proto_library.bzl", "cc_proto_library")
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
    name = "lsm6dso_emb",
    srcs = ["lsm6dso.emb"],
    # TODO(#144): Required for cross-compilation, investigate more
    enable_enum_traits = False,
)

cc_library(
    name = "lsm6dso_emb_helper",
    hdrs = ["lsm6dso_emb_helper.h"],
    deps = [":lsm6dso_emb"],
)

cc_library(
    name = "lsm6dso",
    srcs = ["sim_lsm6dso.cc"],
    hdrs = [
        "lsm6dso_emb_helper.h",
        "sim_lsm6dso.h",
    ],
    deps = [
        "//tlbox/hw/drivers/lsm6dso:lsm6dso_emb",
        "@pigweed//pw_bytes",
        "@pigweed//pw_i2c:address",
        "@pigweed//pw_i2c:initiator",
        "@pigweed//pw_status",
    ],
)

cc_test(
    name = "lsm6dso_pw_test",
    srcs = ["lsm6dso_pw_test.cc"],
    deps = [
        "//tlbox/hw/drivers/lsm6dso:lsm6dso_emb",
        "@pigweed//pw_unit_test",
    ],
)

proto_library(
    name = "lsm6dso_proto",
    srcs = ["lsm6dso.proto"],
    visibility = ["//visibility:public"],
)

nanopb_proto_library(
    name = "lsm6dso_nanopb",
    deps = [":lsm6dso_proto"],
)

nanopb_rpc_proto_library(
    name = "lsm6dso_nanopb_rpc",
    nanopb_proto_library_deps = [":lsm6dso_nanopb"],
    deps = [":lsm6dso_proto"],
)

cc_proto_library(
    name = "lsm6dso_cc_proto",
    visibility = ["//visibility:public"],
    deps = [":lsm6dso_proto"],
)

proto_compile(
    name = "lsm6dso_python_compile",
    outputs = [
        "lsm6dso_pb2.py",
        "lsm6dso_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "lsm6dso_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "lsm6dso_py_library",
    srcs = ["lsm6dso_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)
