load("@rules_proto//proto:defs.bzl", "proto_library")
load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("//bzl:py.bzl", "grpc_py_library", "proto_py_library")

proto_library(
    name = "publish_build_event_proto",
    srcs = ["publish_build_event.proto"],
    visibility = ["//visibility:public"],
    deps = [
        "@googleapis//google/api:annotations_proto",
        "@googleapis//google/api:client_proto",
        "@googleapis//google/api:field_behavior_proto",
        "@googleapis//google/devtools/build/v1:build_proto",
        # "@googleapis//google/api:api_proto",
        # "@googleapis//google/devtools/build/v1:v1_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:empty_proto",
    ],
)

# proto_cc_library(
#     name = "publish_build_event_cc_library",
#     srcs = ["publish_build_event.pb.cc"],
#     hdrs = ["publish_build_event.pb.h"],
#     visibility = ["//visibility:public"],
#     deps = ["@com_google_protobuf//:protobuf"],
# )
# 
# proto_compile(
#     name = "publish_build_event_cpp_compile",
#     outputs = [
#         "publish_build_event.grpc.pb.cc",
#         "publish_build_event.grpc.pb.h",
#         "publish_build_event.pb.cc",
#         "publish_build_event.pb.h",
#     ],
#     plugins = [
#         "@build_stack_rules_proto//plugin/builtin:cpp",
#         "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
#     ],
#     proto = "publish_build_event_proto",
#     visibility = ["//visibility:public"],
# )

grpc_py_library(
    name = "publish_build_event_grpc_py_library",
    srcs = ["publish_build_event_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":publish_build_event_py_library"],
)

proto_compile(
    name = "publish_build_event_python_compile",
    outputs = [
        "publish_build_event_pb2.py",
        "publish_build_event_pb2.pyi",
        "publish_build_event_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "publish_build_event_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "publish_build_event_py_library",
    srcs = ["publish_build_event_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)
