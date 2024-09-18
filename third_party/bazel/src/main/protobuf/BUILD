load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//bzl:py.bzl", "proto_py_library")

package(default_visibility = ["//visibility:private"])

proto_library(
    name = "build_proto",
    srcs = ["build.proto"],
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "build_cc_library",
    srcs = ["build.pb.cc"],
    hdrs = ["build.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "build_cpp_compile",
    outputs = [
        "build.pb.cc",
        "build.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "build_proto",
    visibility = ["//visibility:public"],
)

proto_compile(
    name = "build_python_compile",
    outputs = [
        "build_pb2.py",
        "build_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "build_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "build_py_library",
    srcs = ["build_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_library(
    name = "action_cache_proto",
    srcs = ["action_cache.proto"],
    visibility = ["//visibility:public"],
)

proto_library(
    name = "command_line_proto",
    srcs = ["command_line.proto"],
    deps = [":option_filters_proto"],
    visibility = ["//visibility:public"],
)

proto_library(
    name = "failure_details_proto",
    srcs = ["failure_details.proto"],
    deps = ["@com_google_protobuf//:descriptor_proto"],
    visibility = ["//visibility:public"],
)

proto_library(
    name = "invocation_policy_proto",
    srcs = ["invocation_policy.proto"],
    deps = [":strategy_policy_proto"],
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "action_cache_cc_library",
    srcs = ["action_cache.pb.cc"],
    hdrs = ["action_cache.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "action_cache_cpp_compile",
    outputs = [
        "action_cache.pb.cc",
        "action_cache.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "action_cache_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "command_line_cc_library",
    srcs = ["command_line.pb.cc"],
    hdrs = ["command_line.pb.h"],
    visibility = ["//visibility:public"],
    deps = [
        ":option_filters_cc_library",
        "@com_google_protobuf//:protobuf",
    ],
)

proto_compile(
    name = "command_line_cpp_compile",
    outputs = [
        "command_line.pb.cc",
        "command_line.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "command_line_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "failure_details_cc_library",
    srcs = ["failure_details.pb.cc"],
    hdrs = ["failure_details.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "failure_details_cpp_compile",
    outputs = [
        "failure_details.pb.cc",
        "failure_details.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "failure_details_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "invocation_policy_cc_library",
    srcs = ["invocation_policy.pb.cc"],
    hdrs = ["invocation_policy.pb.h"],
    visibility = ["//visibility:public"],
    deps = [
        ":strategy_policy_cc_library",
        "@com_google_protobuf//:protobuf",
    ],
)

proto_compile(
    name = "invocation_policy_cpp_compile",
    outputs = [
        "invocation_policy.pb.cc",
        "invocation_policy.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "invocation_policy_proto",
    visibility = ["//visibility:public"],
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

proto_library(
    name = "strategy_policy_proto",
    srcs = ["strategy_policy.proto"],
)

proto_cc_library(
    name = "strategy_policy_cc_library",
    srcs = ["strategy_policy.pb.cc"],
    hdrs = ["strategy_policy.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "strategy_policy_cpp_compile",
    outputs = [
        "strategy_policy.pb.cc",
        "strategy_policy.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "strategy_policy_proto",
    visibility = ["//visibility:public"],
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

proto_library(
    name = "option_filters_proto",
    srcs = ["option_filters.proto"],
)

proto_cc_library(
    name = "option_filters_cc_library",
    srcs = ["option_filters.pb.cc"],
    hdrs = ["option_filters.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "option_filters_cpp_compile",
    outputs = [
        "option_filters.pb.cc",
        "option_filters.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "option_filters_proto",
    visibility = ["//visibility:public"],
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
