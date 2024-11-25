load("//bzl:py.bzl", "py_library", "py_test")

package(default_visibility = ["//visibility:private"])

py_library(
    name = "graph_algorithms",
    srcs = ["graph_algorithms.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//networkx"],
)

py_test(
    name = "graph_algorithms_test",
    srcs = ["graph_algorithms_test.py"],
    deps = [
        ":graph_algorithms",
        "@pip//networkx",
    ],
)
