load("@rules_proto//proto:defs.bzl", "proto_library")
load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("//bzl:py.bzl", "proto_py_library")

proto_library(
    name = "package_load_metrics_proto",
    srcs = ["package_load_metrics.proto"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:duration_proto"],
)

proto_cc_library(
    name = "package_load_metrics_cc_library",
    srcs = ["package_load_metrics.pb.cc"],
    hdrs = ["package_load_metrics.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "package_load_metrics_cpp_compile",
    outputs = [
        "package_load_metrics.pb.cc",
        "package_load_metrics.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "package_load_metrics_proto",
    visibility = ["//visibility:public"],
)

proto_compile(
    name = "package_load_metrics_python_compile",
    outputs = [
        "package_load_metrics_pb2.py",
        "package_load_metrics_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "package_load_metrics_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "package_load_metrics_py_library",
    srcs = ["package_load_metrics_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

package(default_visibility = ["//visibility:private"])
