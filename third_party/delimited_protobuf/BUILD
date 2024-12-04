load("//bzl:py.bzl", "py_library", "py_test")

package(default_visibility = ["//visibility:private"])

py_library(
    name = "delimited_protobuf",
    srcs = ["delimited_protobuf.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@com_google_protobuf//:protobuf_python",
        "@pip//protobuf",
    ],
)

py_test(
    name = "delimited_protobuf_test",
    srcs = ["delimited_protobuf_test.py"],
    deps = [
        ":delimited_protobuf",
        "//examples/basic:hello_py_library",
    ],
)
