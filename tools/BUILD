load("@pip//:requirements.bzl", "requirement")  # '@pip' must match configured pip hub_name
load("@rules_multirun//:defs.bzl", "command", "multirun")
load("@rules_mypy//mypy:mypy.bzl", "mypy_cli")
load("//bzl:py.bzl", "py_binary", "py_library")

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
