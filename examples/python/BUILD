load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "hello",
    srcs = ["hello.py"],
    visibility = ["//:__subpackages__"],
)
