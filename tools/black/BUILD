load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "black",
    srcs = ["black.py"],
    data = ["//:pyproject.toml"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//tools:utils",
        "@pip//black",
    ],
)
