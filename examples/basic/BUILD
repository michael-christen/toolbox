load("@aspect_rules_py//py:defs.bzl", "py_binary", "py_library", "py_test")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("@rules_cc//cc:defs.bzl", "cc_library")
load("@rules_python//python:proto.bzl", "py_proto_library")
load("@crate_index//:defs.bzl", "aliases", "all_crate_deps")
load("@rules_rust//rust:defs.bzl", "rust_binary", "rust_doc")

rust_binary(
    name = "hello_world",
    srcs = ["src/main.rs"],
    aliases = aliases(),
    deps = [
        "@crate_index//:ferris-says",
    ],
    # XXX: Not getting to work ...
    # deps = all_crate_deps(),
    # proc_macro_deps = all_crate_deps(
    #     proc_macro = True,
    # ),
)

rust_doc(
    name = "hello_world_doc",
    crate = ":hello_world",
)

proto_library(
    name = "hello_proto",
    srcs = ["hello.proto"],
    visibility = ["//visibility:public"],
)

cc_proto_library(
    name = "hello_cc_proto",
    visibility = [
        "//examples/basic/app:__subpackages__",
    ],
    deps = [":hello_proto"],
)

py_proto_library(
    name = "hello_py_pb2",
    deps = [":hello_proto"],
)

py_test(
    name = "hello_test",
    srcs = ["hello_test.py"],
    deps = [
        "//examples/basic:hello_py_pb2",
    ],
)

package(default_visibility = ["//visibility:private"])

py_library(
    name = "main",
    srcs = ["main.py"],
    visibility = ["//:__subpackages__"],
)
