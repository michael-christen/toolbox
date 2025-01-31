load("@pip//:requirements.bzl", "all_requirements")
load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

# Execute via:
# bazel run tools/jupyter/jupyter.venv
# .tools+jupyter+jupyter.venv/bin/python -m jupyter notebook
#
# XXX: Only importing from sys.path, not the generated bazel libraries
py_binary(
    name = "jupyter",
    srcs = ["jupyter.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip//notebook",
        "//tools:git_utils",
    ] + all_requirements,
)
