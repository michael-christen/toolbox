load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "isort",
    srcs = ["isort.py"],
    data = ["//:pyproject.toml"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//tools:utils",
        "@pip//isort",
    ],
)
