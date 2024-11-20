load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

filegroup(
    name = "python_source",
    srcs = glob(["*.py"]) + [
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "bazel_parser",
    srcs = ["bazel_parser.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//tools:bazel_utils",
        "@pip//networkx",
    ],
)
