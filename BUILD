# Load various rules so that we can have bazel download
# various rulesets and dependencies.
# The `load` statement imports the symbol for the rule, in the defined
# ruleset. When the symbol is loaded you can use the rule.
load("@bazel_gazelle//:def.bzl", "gazelle", "gazelle_binary")
load("@pip//:requirements.bzl", "all_whl_requirements")

# XXX: Get gazelle to use aspect_rules_py instead of rules_python?
# load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load("@rules_python_gazelle_plugin//manifest:defs.bzl", "gazelle_python_manifest")
load("@rules_python_gazelle_plugin//modules_mapping:def.bzl", "modules_mapping")

compile_pip_requirements(
    name = "requirements",
    requirements_in = "requirements.in",
    requirements_txt = "requirements_lock.txt",
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

gazelle_binary(
    name = "gazelle_bin",
    languages = [
        "@bazel_gazelle//language/bazel/visibility",  # bazel visibility rules
        "@bazel_gazelle//language/go",  # Built-in rule from gazelle for Golang
        "@bazel_gazelle//language/proto",  # Built-in rule from gazelle for Protos
        # Any languages that depend on the proto plugin must come after it
        "@rules_python_gazelle_plugin//python:python",  # Use gazelle from rules_python
        "@build_stack_rules_proto//language/protobuf",  # Protobuf language generation
        # TODO: Add buf suppport
        # "@rules_buf//gazelle/buf:buf",  # Generates buf lint and buf breaking detection rules
    ],
)

# Our gazelle target points to the python gazelle binary.
# This is the simple case where we only need one language supported.
# If you also had proto, go, or other gazelle-supported languages,
# you would also need a gazelle_binary rule.
# See https://github.com/bazelbuild/bazel-gazelle/blob/master/extend.rst#example
gazelle(
    name = "gazelle",
    args = [
        "-proto_configs=gazelle_proto_config.yaml",
    ],
    gazelle = ":gazelle_bin",
)

# https://github.com/bazelbuild/bazel-gazelle#directives
# https://github.com/bazelbuild/rules_python/blob/main/gazelle/README.md#directives

# Make a py_library per python file
# gazelle:python_generation_mode file

# Disable BUILD.bazel files
# gazelle:build_file_name BUILD

# Exclude these folders from gazelle generation
# gazelle:exclude venv

# Don't use go
# gazelle:go_generate_proto false

# Generate 1 proto rule per file
# gazelle:proto file

# Set default BUILD rule visibility
# gazelle:default_visibility //visibility:private

# Tell gazelle where to find imports
# gazelle:resolve py google.protobuf.message @com_google_protobuf//:protobuf_python

# TODO: Setup nanopb
# kgazelle:resolve proto nanopb.proto @com_github_nanopb_nanopb//:nanopb_proto

# XXX: Figure out a way to not need these
# gazelle:resolve py examples.basic.hello_pb2 //examples/basic:hello_py_library

package(default_visibility = ["//visibility:private"])
