load("@build_stack_rules_proto//rules/py:proto_py_library.bzl", "proto_py_library")
load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("@aspect_rules_py//py:defs.bzl", "py_binary", "py_test")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("@rules_cc//cc:defs.bzl", "cc_library")
load("@crate_index//:defs.bzl", "aliases", "all_crate_deps")
load("@rules_rust//rust:defs.bzl", "rust_binary", "rust_doc")

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
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "hello_proto",
    visibility = ["//visibility:public"],
)

proto_compile(
    name = "hello_python_compile",
    outputs = [
        "hello_pb2.py",
        "hello_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
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

proto_py_library(
    name = "hello_py_library",
    srcs = ["hello_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

# XXX: Fails with hermetic gcc
# - external/gcc_toolchain_x86_64/bin/gcc: line 24: realpath: command not found
# rust_binary(
#     name = "hello_world",
#     srcs = ["src/main.rs"],
#     aliases = aliases(),
#     deps = [
#         "@crate_index//:ferris-says",
#     ],
#     # TODO: Get rust dependencies working
#     # deps = all_crate_deps(),
#     # proc_macro_deps = all_crate_deps(
#     #     proc_macro = True,
#     # ),
# )
# 
# rust_doc(
#     name = "hello_world_doc",
#     crate = ":hello_world",
# )

py_test(
    name = "hello_test",
    srcs = ["hello_test.py"],
    deps = [
        "//examples/basic:hello_py_library",
    ],
)

py_binary(
    name = "main",
    srcs = ["main.py"],
    visibility = ["//:__subpackages__"],
)
