load("//bzl:py.bzl", "py_binary")

py_binary(
    name = "sphinx_build_wrapper",
    srcs = ["sphinx_build_wrapper.py"],
    visibility = ["//visibility:public"],
    deps = ["@pip//sphinx"],
)

package(default_visibility = ["//visibility:private"])
