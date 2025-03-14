load("@rules_proto//proto:defs.bzl", "proto_library")
load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("@pip//:requirements.bzl", "requirement")  # '@pip' must match configured pip hub_name
load("@rules_multirun//:defs.bzl", "command", "multirun")
load("@rules_mypy//mypy:mypy.bzl", "mypy_cli")
load("//bzl:py.bzl", "proto_py_library", "py_binary", "py_library", "py_test")

package(default_visibility = ["//visibility:private"])

command(
    name = "isort_format",
    args = ["--dont-follow-links"],
    command = "//tools/isort",
    environment = {"USE_TARGET_FROM_ENV": "true"},
)

command(
    name = "isort_check",
    args = [
        "--check",
        "--dont-follow-links",
    ],
    command = "//tools/isort",
    environment = {"USE_TARGET_FROM_ENV": "true"},
)

command(
    name = "black_format",
    command = "//tools/black",
    environment = {"USE_TARGET_FROM_ENV": "true"},
)

command(
    name = "black_check",
    args = ["--check"],
    command = "//tools/black",
    environment = {"USE_TARGET_FROM_ENV": "true"},
)

# Only checks, just invoke the same way in both usages
command(
    name = "flake8",
    command = "//tools/flake8",
    environment = {"USE_TARGET_FROM_ENV": "true"},
)

multirun(
    name = "format",
    # Buffer the output of the commands and print it after each command has finished.
    buffer_output = True,
    commands = [
        # Sort imports
        "isort_format",
        # Autoformat
        "black_format",
        # Ensure flake8 compliance
        "flake8",
    ],
    # Set to 0 to run in parallel, defaults to sequential
    # XXX: Maybe formatting needs to be sequential to prevent data races?
    jobs = 0,
)

multirun(
    name = "check",
    # Buffer the output of the commands and print it after each command has finished.
    buffer_output = True,
    commands = [
        "isort_check",
        "black_check",
        # Ensure flake8 compliance
        "flake8",
    ],
    # Set to 0 to run in parallel, defaults to sequential
    jobs = 0,
)

py_library(
    name = "utils",
    srcs = ["utils.py"],
    visibility = ["//:__subpackages__"],
)

py_library(
    name = "bazel_utils",
    srcs = ["bazel_utils.py"],
    visibility = ["//:__subpackages__"],
    deps = ["//third_party/bazel/src/main/protobuf:build_py_library"],
)

py_binary(
    name = "coverage_baseline",
    srcs = ["coverage_baseline.py"],
    visibility = ["//:__subpackages__"],
)

mypy_cli(
    name = "mypy_cli",
    mypy_requirement = requirement("mypy"),
    deps = [
        "@pip//types_protobuf",
    ],
)

proto_library(
    name = "git_proto",
    srcs = ["git.proto"],
    deps = ["@com_google_protobuf//:timestamp_proto"],
)

py_library(
    name = "git_utils",
    srcs = ["git_utils.py"],
    visibility = ["//:__subpackages__"],
    deps = ["//tools:git_py_library"],
)

py_test(
    name = "git_utils_test",
    srcs = ["git_utils_test.py"],
)

proto_cc_library(
    name = "git_cc_library",
    srcs = ["git.pb.cc"],
    hdrs = ["git.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "git_cpp_compile",
    outputs = [
        "git.pb.cc",
        "git.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "git_proto",
    visibility = ["//visibility:public"],
)

proto_compile(
    name = "git_python_compile",
    outputs = [
        "git_pb2.py",
        "git_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "git_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "git_py_library",
    srcs = ["git_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)
