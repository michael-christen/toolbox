load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("//bzl:py.bzl", "grpc_py_library", "proto_py_library")
load("@io_bazel_rules_go//proto:def.bzl", "go_proto_library")
load("@rules_proto//proto:defs.bzl", "proto_library")

package(default_visibility = ["//visibility:private"])

proto_library(
    name = "jaeger_proto",
    srcs = [
        "model.proto",
        "query.proto",
    ],
    deps = [
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
        "@googleapis//google/api:annotations_proto",
    ],
)

go_proto_library(
    name = "jaeger_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/jaeger",
    proto = ":jaeger_proto",
    deps = [
        "@org_golang_google_genproto_googleapis_api//annotations",
    ],
)

proto_library(
    name = "model_proto",
    srcs = ["model.proto"],
    deps = [
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "query_proto",
    srcs = ["query.proto"],
    deps = [
        "//google/api:api_proto",
        "//proto/jaeger:jaeger_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_cc_library(
    name = "model_cc_library",
    srcs = ["model.pb.cc"],
    hdrs = ["model.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "model_cpp_compile",
    outputs = [
        "model.pb.cc",
        "model.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "model_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "query_cc_library",
    srcs = ["query.pb.cc"],
    hdrs = ["query.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "query_cpp_compile",
    outputs = [
        "query.grpc.pb.cc",
        "query.grpc.pb.h",
        "query.pb.cc",
        "query.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "query_proto",
    visibility = ["//visibility:public"],
)

proto_compile(
    name = "model_python_compile",
    outputs = [
        "model_pb2.py",
        "model_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "model_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "model_py_library",
    srcs = ["model_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "query_grpc_py_library",
    srcs = ["query_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":query_py_library"],
)

proto_compile(
    name = "query_python_compile",
    outputs = [
        "query_pb2.py",
        "query_pb2.pyi",
        "query_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "query_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "query_py_library",
    srcs = ["query_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)
