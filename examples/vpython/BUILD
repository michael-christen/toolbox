load("//bzl:py.bzl", "py_binary", "py_library")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "basic_pendulum",
    srcs = ["basic_pendulum.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//vpython"],
)

py_library(
    name = "group",
    srcs = ["group.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//vpython"],
)

py_binary(
    name = "hello_world",
    srcs = ["hello_world.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//vpython"],
)

py_binary(
    name = "inverted_pendulum",
    srcs = ["inverted_pendulum.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip//numpy",
        "@pip//vpython",
    ],
)

py_binary(
    name = "sliding_pendulum",
    srcs = ["sliding_pendulum.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//vpython"],
)
