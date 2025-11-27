# Load various rules so that we can have bazel download
# various rulesets and dependencies.
# The `load` statement imports the symbol for the rule, in the defined
# ruleset. When the symbol is loaded you can use the rule.
load("@bazel_gazelle//:def.bzl", "gazelle")
load("@npm//:defs.bzl", "npm_link_all_packages")
load("@pip//:requirements.bzl", "all_whl_requirements")
load("@rules_python_gazelle_plugin//manifest:defs.bzl", "gazelle_python_manifest")
load("@rules_python_gazelle_plugin//modules_mapping:def.bzl", "modules_mapping")
load("@rules_uv//uv:pip.bzl", "pip_compile")
load("@rules_uv//uv:venv.bzl", "create_venv")

package(default_visibility = ["//visibility:private"])

exports_files(
    [
        ".flake8",
        ".prettierrc",
        ".clang-format",
        ".clang-tidy",
        "multitool.lock.json",
        "mypy.ini",
        "pytest.ini",
        "pyproject.toml",
    ],
    visibility = ["//visibility:public"],
)

pip_compile(
    name = "requirements",
    # https://bazel.build/reference/be/common-definitions
    requirements_in = "requirements.in",
    requirements_txt = "requirements_lock.txt",
    tags = [
        # Don't want to type-check requirements building
        "no-mypy",
        # Avoid in flake detection
        "skip-large-tests",
    ],
)

# bazel run //:create_venv
# venv/bin/<cmd>
#
# Note that you should likely be able to modify non-generated source and see
# this reflected by venv binary references, etc.
create_venv(
    name = "create_venv",
    destination_folder = "venv",
    requirements_txt = "//:requirements_lock.txt",
)

# This repository rule fetches the metadata for python packages we
# depend on. That data is required for the gazelle_python_manifest
# rule to update our manifest file.
# To see what this rule does, try `bazel run @modules_map//:print`
modules_mapping(
    name = "modules_map",
    exclude_patterns = [
        "^_|(\\._)+",  # This is the default.
        "(\\.tests)+",  # Add a custom one to get rid of the psutil tests.
    ],
    wheels = all_whl_requirements,
)

# Gazelle python extension needs a manifest file mapping from
# an import to the installed package that provides it.
# This macro produces two targets:
# - //:gazelle_python_manifest.update can be used with `bazel run`
#   to recalculate the manifest
# - //:gazelle_python_manifest.test is a test target ensuring that
#   the manifest doesn't need to be updated
gazelle_python_manifest(
    name = "gazelle_python_manifest",
    modules_mapping = ":modules_map",
    pip_repository_name = "pip",
    # NOTE: We can pass a list just like in `bzlmod_build_file_generation` example
    # but we keep a single target here for regression testing.
    requirements = "//:requirements_lock.txt",
)

# XXX: Likely need this for languages
# gazelle_binary(
#     name = "gazelle_bin",
#     languages = [
#         "@bazel_gazelle//language/bazel/visibility",  # bazel visibility rules
#         "@bazel_gazelle//language/go",  # Built-in rule from gazelle for Golang
#         "@bazel_gazelle//language/proto",  # Built-in rule from gazelle for Protos
#         # Any languages that depend on the proto plugin must come after it
#         "@rules_python_gazelle_plugin//python:python",  # Use gazelle from rules_python
#         "@build_stack_rules_proto//language/protobuf",  # Protobuf language generation
#         # TODO: Add buf suppport
#         # "@rules_buf//gazelle/buf:buf",  # Generates buf lint and buf breaking detection rules
#     ],
# )

# Our gazelle target points to the python gazelle binary.
# This is the simple case where we only need one language supported.
# If you also had proto, go, or other gazelle-supported languages,
# you would also need a gazelle_binary rule.
# See https://github.com/bazelbuild/bazel-gazelle/blob/master/extend.rst#example
gazelle(
    name = "gazelle",
    # XXX: How are languages presented?
    # XXX: Re-enable ...
    # args = [
    #     "-proto_configs=gazelle_proto_config.yaml",
    # ],
    # gazelle = ":gazelle_bin",
    gazelle = "@multitool//tools/gazelle",
)

# https://github.com/bazelbuild/bazel-gazelle#directives
# https://github.com/bazelbuild/rules_python/blob/main/gazelle/README.md#directives

# Make a py_library per python file
# gazelle:python_generation_mode file

# Disable BUILD.bazel files
# gazelle:build_file_name BUILD

# Exclude these folders from gazelle generation
# gazelle:exclude venv
# XXX: Avoid gazelle on these directories
# gazelle:exclude apps/csv-to-sheets
# gazelle:exclude apps/ical
# gazelle:exclude examples/pyglet

# Don't use go
# gazelle:go_generate_proto false

# Generate 1 proto rule per file
# gazelle:proto file

# Set default BUILD rule visibility
# gazelle:default_visibility //visibility:private

# Tell gazelle where to find imports
# gazelle:resolve py google.protobuf.message @com_google_protobuf//:protobuf_python

# Use our own rules
# gazelle:map_kind py_binary py_binary //bzl:py.bzl
# gazelle:map_kind py_library py_library //bzl:py.bzl
# gazelle:map_kind py_test py_test //bzl:py.bzl
# gazelle:map_kind grpc_py_library grpc_py_library //bzl:py.bzl
# gazelle:map_kind proto_py_library proto_py_library //bzl:py.bzl

# TODO: Figure out a way to not need these
# gazelle:resolve py hw_services.sbr.sbr_pb2 //hw_services/sbr:sbr_py_library
# gazelle:resolve py examples.basic.hello_pb2 //examples/basic:hello_py_library
# gazelle:resolve py examples.basic.hello_pb2_grpc //examples/basic:hello_grpc_py_library
# gazelle:resolve py third_party.bazel.src.main.protobuf.build_pb2 //third_party/bazel/src/main/protobuf:build_py_library
# gazelle:resolve py third_party.bazel.proto.build_event_stream_pb2 //third_party/bazel/proto:build_event_stream_py_library
# gazelle:resolve proto pw_protobuf_protos/common.proto @pigweed//pw_protobuf:common_proto
# gazelle:resolve py examples.pigweed.modules.blinky.blinky_pb2 //examples/pigweed/modules/blinky:blinky_pb2
# gazelle:resolve py tools.git_pb2 //tools:git_py_library
# gazelle:resolve py pw_cli @pigweed//pw_system/py:pw_system_lib
# gazelle:resolve py pw_system.console @pigweed//pw_system/py:pw_system_lib
# gazelle:resolve py pw_system.device @pigweed//pw_system/py:pw_system_lib
# gazelle:resolve py pw_system.device_connection @pigweed//pw_system/py:pw_system_lib

npm_link_all_packages(name = "node_modules")

filegroup(
    name = "python_source",
    srcs = glob(
        ["*.py"],
        allow_empty = True,
    ) + [
        "//apps:python_source",
        "//examples/basic:python_source",
        "//examples/bazel:python_source",
        "//examples/pigweed/modules/blinky:python_source",
        "//third_party/pigweed/tools:python_source",
    ],
    visibility = ["//visibility:public"],
)

alias(
    name = "format",
    actual = "//tools/format",
)
