load("@rules_proto//proto:defs.bzl", "proto_library")
load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("//bzl:py.bzl", "proto_py_library")

proto_library(
    name = "build_event_stream_proto",
    srcs = ["build_event_stream.proto"],
    visibility = ["//visibility:public"],
    deps = [
        "//third_party/bazel/src/main/java/com/google/devtools/build/lib/packages/metrics:package_load_metrics_proto",
        "//third_party/bazel/src/main/protobuf:action_cache_proto",
        "//third_party/bazel/src/main/protobuf:command_line_proto",
        "//third_party/bazel/src/main/protobuf:failure_details_proto",
        "//third_party/bazel/src/main/protobuf:invocation_policy_proto",
        "@com_google_protobuf//:any_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_cc_library(
    name = "build_event_stream_cc_library",
    srcs = ["build_event_stream.pb.cc"],
    hdrs = ["build_event_stream.pb.h"],
    visibility = ["//visibility:public"],
    deps = [
        "//third_party/bazel/src/main/java/com/google/devtools/build/lib/packages/metrics:package_load_metrics_cc_library",
        "//third_party/bazel/src/main/protobuf:action_cache_cc_library",
        "//third_party/bazel/src/main/protobuf:command_line_cc_library",
        "//third_party/bazel/src/main/protobuf:failure_details_cc_library",
        "//third_party/bazel/src/main/protobuf:invocation_policy_cc_library",
        "@com_google_protobuf//:protobuf",
    ],
)

proto_compile(
    name = "build_event_stream_cpp_compile",
    outputs = [
        "build_event_stream.pb.cc",
        "build_event_stream.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "build_event_stream_proto",
    visibility = ["//visibility:public"],
)

proto_compile(
    name = "build_event_stream_python_compile",
    outputs = [
        "build_event_stream_pb2.py",
        "build_event_stream_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "build_event_stream_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "build_event_stream_py_library",
    srcs = ["build_event_stream_pb2.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//third_party/bazel/src/main/java/com/google/devtools/build/lib/packages/metrics:package_load_metrics_py_library",
        "//third_party/bazel/src/main/protobuf:action_cache_py_library",
        "//third_party/bazel/src/main/protobuf:command_line_py_library",
        "//third_party/bazel/src/main/protobuf:failure_details_py_library",
        "//third_party/bazel/src/main/protobuf:invocation_policy_py_library",
        "@com_google_protobuf//:protobuf_python",
    ],
)

package(default_visibility = ["//visibility:private"])
