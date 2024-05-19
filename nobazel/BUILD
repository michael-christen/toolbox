load("@rules_proto//proto:defs.bzl", "proto_library")
load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")

package(default_visibility = ["//visibility:private"])

proto_library(
    name = "hello_proto",
    srcs = ["hello.proto"],
    visibility = ["//visibility:public"],
)

proto_compile(
    name = "hello_cpp_compile",
    outputs = [
        "hello.pb.cc",
        "hello.pb.h",
        "hello.grpc.pb.cc",
        "hello.grpc.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "hello_proto",
    visibility = ["//visibility:public"],
)

proto_compile(
    name = "hello_python_compile",
    outputs = [
        "hello_pb2.py",
        "hello_pb2.pyi",
        "hello_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "hello_proto",
    visibility = ["//visibility:public"],
)
