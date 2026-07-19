load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "oras_example",
    srcs = ["oras_example.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip//oras",
        "@pip//requests",
    ],
)
