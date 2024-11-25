load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "bep_reader",
    srcs = ["bep_reader.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//third_party/bazel/proto:build_event_stream_py_library",
        "//third_party/delimited_protobuf",
        "@pip//tabulate",
    ],
)
