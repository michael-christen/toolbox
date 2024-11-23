load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("//bzl:py.bzl", "grpc_py_library", "proto_py_library")
load("@io_bazel_rules_go//proto:def.bzl", "go_proto_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//proto:defs.bzl", "ts_proto_library")

proto_library(
    name = "common_proto",
    srcs = [
        "common.proto",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

go_proto_library(
    name = "common_go_proto",
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/api/v1/common",
    proto = ":common_proto",
    visibility = ["//visibility:public"],
)

ts_proto_library(
    name = "common_ts_proto",
    proto = ":common_proto",
    visibility = ["//visibility:public"],
    deps = [
        "//proto:duration_ts_proto",
        "//proto:grpc_status_ts_proto",
        "//proto:timestamp_ts_proto",
    ],
)

proto_library(
    name = "api_v1_proto",
    srcs = [
        "action.proto",
        "file.proto",
        "invocation.proto",
        "log.proto",
        "remote_runner.proto",
        "service.proto",
        "target.proto",
        "workflow.proto",
    ],
    visibility = ["//visibility:public"],
    deps = [
        ":common_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
        "@googleapis//google/rpc:status_proto",
    ],
)

go_proto_library(
    name = "api_v1_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/api/v1",
    proto = ":api_v1_proto",
    visibility = ["//visibility:public"],
    deps = [
        ":common_go_proto",
        "@org_golang_google_genproto_googleapis_rpc//status",
    ],
)

package(default_visibility = ["//visibility:private"])

proto_library(
    name = "action_proto",
    srcs = ["action.proto"],
    visibility = ["//visibility:public"],
    deps = ["//proto/api/v1:v1_proto"],
)

proto_library(
    name = "file_proto",
    srcs = ["file.proto"],
    visibility = ["//visibility:public"],
)

proto_library(
    name = "invocation_proto",
    srcs = ["invocation.proto"],
    visibility = ["//visibility:public"],
    deps = ["//proto/api/v1:v1_proto"],
)

proto_library(
    name = "log_proto",
    srcs = ["log.proto"],
    visibility = ["//visibility:public"],
)

proto_library(
    name = "remote_runner_proto",
    srcs = ["remote_runner.proto"],
    visibility = ["//visibility:public"],
    deps = ["//google/rpc:rpc_proto"],
)

proto_library(
    name = "service_proto",
    srcs = ["service.proto"],
    visibility = ["//visibility:public"],
    deps = ["//proto/api/v1:v1_proto"],
)

proto_library(
    name = "target_proto",
    srcs = ["target.proto"],
    visibility = ["//visibility:public"],
    deps = ["//proto/api/v1:v1_proto"],
)

proto_library(
    name = "workflow_proto",
    srcs = ["workflow.proto"],
    visibility = ["//visibility:public"],
    deps = ["//google/rpc:rpc_proto"],
)

proto_cc_library(
    name = "action_cc_library",
    srcs = ["action.pb.cc"],
    hdrs = ["action.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "action_cpp_compile",
    outputs = [
        "action.pb.cc",
        "action.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "action_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "common_cc_library",
    srcs = ["common.pb.cc"],
    hdrs = ["common.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "common_cpp_compile",
    outputs = [
        "common.pb.cc",
        "common.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "common_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "file_cc_library",
    srcs = ["file.pb.cc"],
    hdrs = ["file.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "file_cpp_compile",
    outputs = [
        "file.pb.cc",
        "file.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "file_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "invocation_cc_library",
    srcs = ["invocation.pb.cc"],
    hdrs = ["invocation.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "invocation_cpp_compile",
    outputs = [
        "invocation.pb.cc",
        "invocation.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "invocation_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "log_cc_library",
    srcs = ["log.pb.cc"],
    hdrs = ["log.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "log_cpp_compile",
    outputs = [
        "log.pb.cc",
        "log.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "log_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "remote_runner_cc_library",
    srcs = ["remote_runner.pb.cc"],
    hdrs = ["remote_runner.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "remote_runner_cpp_compile",
    outputs = [
        "remote_runner.pb.cc",
        "remote_runner.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "remote_runner_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "service_cc_library",
    srcs = ["service.pb.cc"],
    hdrs = ["service.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "service_cpp_compile",
    outputs = [
        "service.grpc.pb.cc",
        "service.grpc.pb.h",
        "service.pb.cc",
        "service.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "service_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "target_cc_library",
    srcs = ["target.pb.cc"],
    hdrs = ["target.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "target_cpp_compile",
    outputs = [
        "target.pb.cc",
        "target.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "target_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "workflow_cc_library",
    srcs = ["workflow.pb.cc"],
    hdrs = ["workflow.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "workflow_cpp_compile",
    outputs = [
        "workflow.pb.cc",
        "workflow.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "workflow_proto",
    visibility = ["//visibility:public"],
)

proto_compile(
    name = "action_python_compile",
    outputs = [
        "action_pb2.py",
        "action_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "action_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "action_py_library",
    srcs = ["action_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "common_python_compile",
    outputs = [
        "common_pb2.py",
        "common_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "common_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "common_py_library",
    srcs = ["common_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "file_python_compile",
    outputs = [
        "file_pb2.py",
        "file_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "file_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "file_py_library",
    srcs = ["file_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "invocation_python_compile",
    outputs = [
        "invocation_pb2.py",
        "invocation_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "invocation_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "invocation_py_library",
    srcs = ["invocation_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "log_python_compile",
    outputs = [
        "log_pb2.py",
        "log_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "log_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "log_py_library",
    srcs = ["log_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "remote_runner_python_compile",
    outputs = [
        "remote_runner_pb2.py",
        "remote_runner_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "remote_runner_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "remote_runner_py_library",
    srcs = ["remote_runner_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "service_grpc_py_library",
    srcs = ["service_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":service_py_library"],
)

proto_compile(
    name = "service_python_compile",
    outputs = [
        "service_pb2.py",
        "service_pb2.pyi",
        "service_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "service_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "service_py_library",
    srcs = ["service_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "target_python_compile",
    outputs = [
        "target_pb2.py",
        "target_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "target_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "target_py_library",
    srcs = ["target_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "workflow_python_compile",
    outputs = [
        "workflow_pb2.py",
        "workflow_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "workflow_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "workflow_py_library",
    srcs = ["workflow_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)
