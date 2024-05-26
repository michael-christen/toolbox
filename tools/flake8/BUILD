load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "flake8",
    srcs = ["flake8.py"],
    data = ["//:.flake8"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//tools:utils",
        "@pip//flake8",
    ],
)
