load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("@com_google_protobuf//bazel:cc_proto_library.bzl", "cc_proto_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//bzl:py.bzl", "proto_py_library")

package(default_visibility = ["//visibility:private"])

proto_library(
    name = "action_cache_proto",
    srcs = ["action_cache.proto"],
    visibility = ["//visibility:public"],
)

proto_library(
    name = "build_event_stream_proto",
    srcs = ["build_event_stream.proto"],
    visibility = ["//visibility:public"],
    deps = [
        ":action_cache_proto",
        ":command_line_proto",
        ":failure_details_proto",
        ":invocation_policy_proto",
        ":package_load_metrics_proto",
        "@com_google_protobuf//:any_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "command_line_proto",
    srcs = ["command_line.proto"],
    visibility = ["//visibility:public"],
    deps = [":option_filters_proto"],
)

proto_library(
    name = "failure_details_proto",
    srcs = ["failure_details.proto"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:descriptor_proto"],
)

proto_library(
    name = "invocation_policy_proto",
    srcs = ["invocation_policy.proto"],
    visibility = ["//visibility:public"],
    deps = [":strategy_policy_proto"],
)

proto_library(
    name = "option_filters_proto",
    srcs = ["option_filters.proto"],
    visibility = ["//visibility:public"],
)

proto_library(
    name = "package_load_metrics_proto",
    srcs = ["package_load_metrics.proto"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:duration_proto"],
)

proto_library(
    name = "strategy_policy_proto",
    srcs = ["strategy_policy.proto"],
)

proto_library(
    name = "spawn_proto",
    srcs = ["spawn.proto"],
    deps = [
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

cc_proto_library(
    name = "action_cache_cc_proto",
    visibility = ["//visibility:public"],
    deps = [":action_cache_proto"],
)

cc_proto_library(
    name = "build_event_stream_cc_proto",
    visibility = ["//visibility:public"],
    deps = [":build_event_stream_proto"],
)

cc_proto_library(
    name = "command_line_cc_proto",
    visibility = ["//visibility:public"],
    deps = [":command_line_proto"],
)

cc_proto_library(
    name = "failure_details_cc_proto",
    visibility = ["//visibility:public"],
    deps = [":failure_details_proto"],
)

cc_proto_library(
    name = "invocation_policy_cc_proto",
    visibility = ["//visibility:public"],
    deps = [":invocation_policy_proto"],
)

cc_proto_library(
    name = "option_filters_cc_proto",
    visibility = ["//visibility:public"],
    deps = [":option_filters_proto"],
)

cc_proto_library(
    name = "package_load_metrics_cc_proto",
    visibility = ["//visibility:public"],
    deps = [":package_load_metrics_proto"],
)

cc_proto_library(
    name = "strategy_policy_cc_proto",
    visibility = ["//visibility:public"],
    deps = [":strategy_policy_proto"],
)

cc_proto_library(
    name = "spawn_cc_proto",
    visibility = ["//visibility:public"],
    deps = [":spawn_proto"],
)

proto_compile(
    name = "action_cache_python_compile",
    outputs = [
        "action_cache_pb2.py",
        "action_cache_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "action_cache_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "action_cache_py_library",
    srcs = ["action_cache_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
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
        ":action_cache_py_library",
        ":command_line_py_library",
        ":failure_details_py_library",
        ":invocation_policy_py_library",
        ":package_load_metrics_py_library",
        "@com_google_protobuf//:protobuf_python",
    ],
)

proto_compile(
    name = "command_line_python_compile",
    outputs = [
        "command_line_pb2.py",
        "command_line_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "command_line_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "command_line_py_library",
    srcs = ["command_line_pb2.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":option_filters_py_library",
        "@com_google_protobuf//:protobuf_python",
    ],
)

proto_compile(
    name = "failure_details_python_compile",
    outputs = [
        "failure_details_pb2.py",
        "failure_details_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "failure_details_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "failure_details_py_library",
    srcs = ["failure_details_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "invocation_policy_python_compile",
    outputs = [
        "invocation_policy_pb2.py",
        "invocation_policy_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "invocation_policy_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "invocation_policy_py_library",
    srcs = ["invocation_policy_pb2.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":strategy_policy_py_library",
        "@com_google_protobuf//:protobuf_python",
    ],
)

proto_compile(
    name = "option_filters_python_compile",
    outputs = [
        "option_filters_pb2.py",
        "option_filters_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "option_filters_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "option_filters_py_library",
    srcs = ["option_filters_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
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

proto_compile(
    name = "strategy_policy_python_compile",
    outputs = [
        "strategy_policy_pb2.py",
        "strategy_policy_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "strategy_policy_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "strategy_policy_py_library",
    srcs = ["strategy_policy_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "spawn_python_compile",
    outputs = [
        "spawn_pb2.py",
        "spawn_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "spawn_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "spawn_py_library",
    srcs = ["spawn_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)
