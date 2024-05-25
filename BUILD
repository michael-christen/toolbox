# Load various rules so that we can have bazel download
# various rulesets and dependencies.
# The `load` statement imports the symbol for the rule, in the defined
# ruleset. When the symbol is loaded you can use the rule.
load("@bazel_gazelle//:def.bzl", "gazelle_binary")
load("@com_github_bazelbuild_buildtools//buildifier:def.bzl", "buildifier")
load("@pip//:requirements.bzl", "all_whl_requirements")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load("@rules_python_gazelle_plugin//manifest:defs.bzl", "gazelle_python_manifest")
load("@rules_python_gazelle_plugin//modules_mapping:def.bzl", "modules_mapping")
load("@build_stack_rules_proto//rules:proto_gazelle.bzl", "proto_gazelle")

exports_files([
    "pytest.ini",
])

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

# See https://github.com/bazelbuild/bazel-gazelle/blob/master/extend.rst#example
proto_gazelle(
    name = "gazelle",
    args = [
        "-proto_configs=gazelle_proto_config.yaml",
    ],
    command = "update",
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

# Configure aspect_rules_py to be used for py_test, py_binary, py_library
# gazelle:map_kind py_binary py_binary @aspect_rules_py//py:defs.bzl
# gazelle:map_kind py_library py_library @aspect_rules_py//py:defs.bzl
# gazelle:map_kind py_test py_test @aspect_rules_py//py:defs.bzl

# Tell gazelle where to find imports
# gazelle:resolve py google.protobuf.message @com_google_protobuf//:protobuf_python

# Use our own rules
# gazelle:map_kind py_binary py_binary //bzl:py.bzl
# gazelle:map_kind py_library py_library //bzl:py.bzl
# gazelle:map_kind py_test py_test //bzl:py.bzl

package(default_visibility = ["//visibility:private"])

# Run as:
# bazel run //:buildifier -- <args>
buildifier(
    name = "buildifier",
)
# Run buildozer as:
# bazel run --run_under="cd $PWD && " @com_github_bazelbuild_buildtools//buildozer --  <args>
