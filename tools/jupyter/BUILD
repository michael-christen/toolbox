load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "jupyter",
    srcs = ["jupyter.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//notebook"],
)
