load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "isort",
    srcs = ["isort.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//isort"],
)
