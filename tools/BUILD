load("@bazel_env.bzl", "bazel_env")
load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("@multitool//:tools.bzl", MULTITOOL_TOOLS = "TOOLS")
load("@pip//:requirements.bzl", "requirement")  # '@pip' must match configured pip hub_name
load("@rules_multirun//:defs.bzl", "command", "multirun")
load("@rules_mypy//mypy:mypy.bzl", "mypy_cli")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//bzl:py.bzl", "proto_py_library", "py_library", "py_test")

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
    # Maybe formatting needs to be sequential to prevent data races?
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

alias(
    name = "bazel_utils",
    actual = "//tlbox/utils:bazel_utils",
    visibility = ["//:__subpackages__"],
)

alias(
    name = "generate_ccindex",
    actual = "//tlbox/utils:generate_ccindex",
    visibility = ["//:__subpackages__"],
)

alias(
    name = "coverage_baseline",
    actual = "//tlbox/utils:coverage_baseline",
    visibility = ["//:__subpackages__"],
)

mypy_cli(
    name = "mypy_cli",
    mypy_requirement = requirement("mypy"),
    # Must match PYTHON_VERSION in MODULE.bazel
    # LINK(7e463bc3_e4d9_4464_ba39_3217c4a86004)
    python_version = "3.11.9",
    deps = [
        "@pip//types_protobuf",
    ],
)

proto_library(
    name = "git_proto",
    srcs = ["git.proto"],
    deps = ["@com_google_protobuf//:timestamp_proto"],
)

alias(
    name = "git_utils",
    actual = "//tlbox/utils:git_utils",
    visibility = ["//:__subpackages__"],
)

py_test(
    name = "git_utils_test",
    srcs = ["git_utils_test.py"],
    deps = ["//tlbox/utils:git_utils"],
)

cc_proto_library(
    name = "git_cc_proto",
    deps = [":git_proto"],
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

# Rerun `bazel run //tools:bazel_env` if you modify this target
bazel_env(
    name = "bazel_env",
    toolchains = {
        "python": "@rules_python//python:current_py_toolchain",
    },
    tools = {
        "buildifier": "@buildifier_prebuilt//:buildifier",
        "buildozer": "@buildifier_prebuilt//:buildozer",
        "format": "//tools/format:format",
        "python": "$(PYTHON3)",
    } | MULTITOOL_TOOLS,
)
