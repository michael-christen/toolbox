load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@com_google_emboss//:build_defs.bzl", "emboss_cc_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//bzl:cc.bzl", "cc_library")
load("//bzl:py.bzl", "proto_py_library")

package(default_visibility = ["//visibility:private"])

emboss_cc_library(
    name = "lsm6dso_emb",
    srcs = ["lsm6dso.emb"],
)

# XXX: Make a better example elsewhere
# load("@aspect_bazel_lib//lib:write_source_files.bzl", "write_source_files")
# write_source_files(
#     name = "write_emb",
#     files = {
#         "lsm6dso_generated.emb.h": ":lsm6dso_emb",
#     },
# )

cc_library(
    name = "example",
    srcs = ["example.cc"],
    hdrs = ["example.h"],
    deps = [":lsm6dso_emb"],
)

proto_library(
    name = "lsm6dso_proto",
    srcs = ["lsm6dso.proto"],
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "lsm6dso_cc_library",
    srcs = ["lsm6dso.pb.cc"],
    hdrs = ["lsm6dso.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "lsm6dso_cpp_compile",
    outputs = [
        "lsm6dso.pb.cc",
        "lsm6dso.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "lsm6dso_proto",
    visibility = ["//visibility:public"],
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
