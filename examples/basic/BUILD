load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@rules_proto//proto:defs.bzl", "proto_library")

# load("@crate_index//:defs.bzl", "aliases", "all_crate_deps")
load("@rules_rust//rust:defs.bzl", "rust_binary", "rust_library", "rust_test", "rust_doc")
load("//bzl:py.bzl", "grpc_py_library", "proto_py_library", "py_binary", "py_image", "py_test")

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

proto_cc_library(
    name = "hello_cc_library",
    srcs = ["hello.pb.cc"],
    hdrs = ["hello.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

rust_library(
    name = "lib",
    srcs = ["src/lib.rs"],
)

rust_test(
    name = "lib_test",
    crate = ":lib",
)

rust_binary(
    name = "hello_world",
    srcs = ["src/main.rs"],
    deps = [
        "@crate_index//:ferris-says",
    ],
    # TODO: Get rust dependencies working
    # aliases = aliases(),
    # deps = all_crate_deps(),
    # proc_macro_deps = all_crate_deps(
    #     proc_macro = True,
    # ),
)

rust_doc(
    name = "hello_world_doc",
    crate = ":hello_world",
)

py_test(
    name = "hello_test",
    srcs = ["hello_test.py"],
    deps = ["//examples/basic:hello_py_library"],
)

py_binary(
    name = "main",
    srcs = ["main.py"],
    visibility = ["//:__subpackages__"],
)

py_binary(
    name = "server",
    srcs = ["server.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//examples/basic:hello_grpc_py_library",
        "//examples/basic:hello_py_library",
        "@pip//grpcio",
    ],
)

# Build and run this image with
#     bazel run //examples/basic:sever_img_load_docker
#     docker run --rm server:latest
py_image(
    name = "server_img",
    binary = ":server",
    image_tags = ["server:latest"],
)

py_binary(
    name = "client",
    srcs = ["client.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//examples/basic:hello_grpc_py_library",
        "//examples/basic:hello_py_library",
        "@pip//grpcio",
    ],
)

# Build and run this image with
#     bazel run //examples/basic:client_img_load_docker
#     docker run --rm client:latest
py_image(
    name = "client_img",
    binary = ":client",
    image_tags = ["client:latest"],
)

py_test(
    name = "grpc_test",
    srcs = ["grpc_test.py"],
    deps = [
        ":client",
        ":server",
        "//examples/basic:hello_py_library",
    ],
    # XXX: How to expect_failure
)

grpc_py_library(
    name = "hello_grpc_py_library",
    srcs = ["hello_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":hello_py_library"],
)

proto_py_library(
    name = "hello_py_library",
    srcs = ["hello_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)
