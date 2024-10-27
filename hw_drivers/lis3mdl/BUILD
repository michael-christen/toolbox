load("@rules_proto//proto:defs.bzl", "proto_library")
load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("//bzl:py.bzl", "proto_py_library")
load("@com_google_emboss//:build_defs.bzl", "emboss_cc_library")
load("//bzl:cc.bzl", "cc_library", "cc_test")

emboss_cc_library(
    name = "lis3mdl_emb",
    srcs = ["lis3mdl.emb"],
)

cc_library(
    name = "lis3mdl",
    srcs = ["lis3mdl.cc"],
    hdrs = ["lis3mdl.h"],
    deps = [
        ":lis3mdl_emb",
        ":lis3mdl_cc_library",
    ],
)

cc_test(
    name = "lis3mdl_test",
    srcs = ["lis3mdl_test.cc"],
    deps = [
        ":lis3mdl_emb",
        ":lis3mdl",
        ":lis3mdl_cc_library",
        "//testing:catch_main",
    ],
)

package(default_visibility = ["//visibility:private"])

proto_library(
    name = "lis3mdl_proto",
    srcs = ["lis3mdl.proto"],
    visibility = ["//visibility:public"],
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
