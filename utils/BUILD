load("//bzl:py.bzl", "py_binary", "py_library", "py_test")

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

py_binary(
    name = "bep_reader",
    srcs = ["bep_reader.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//third_party/bazel/proto:build_event_stream_py_library",
        "//third_party/delimited_protobuf:util",
        "@pip//tabulate",
    ],
)
