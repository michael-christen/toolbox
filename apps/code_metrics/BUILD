load("//bzl:py.bzl", "py_binary")

py_binary(
    name = "main",
    srcs = ["main.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//tools:bazel_utils",
        "//tools:git_utils",
    ],
)

package(default_visibility = ["//visibility:private"])
