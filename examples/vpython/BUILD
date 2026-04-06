load("//bzl:py.bzl", "py_binary", "py_library")

# gazelle:resolve py vpython //examples/vpython:vpython_stub

package(default_visibility = ["//visibility:private"])

py_library(
    name = "pkg_resources",
    srcs = ["pkg_resources.py"],
    imports = ["."],
    visibility = ["//:__subpackages__"],
)

py_library(
    name = "vpython_stub",
    visibility = ["//visibility:public"],
    deps = [
        ":pkg_resources",
        "@pip//vpython",
    ],
)

py_binary(
    name = "basic_pendulum",
    srcs = ["basic_pendulum.py"],
    visibility = ["//:__subpackages__"],
    deps = ["//examples/vpython:vpython_stub"],
)

py_library(
    name = "group",
    srcs = ["group.py"],
    visibility = ["//:__subpackages__"],
    deps = ["//examples/vpython:vpython_stub"],
)

py_binary(
    name = "hello_world",
    srcs = ["hello_world.py"],
    visibility = ["//:__subpackages__"],
    deps = ["//examples/vpython:vpython_stub"],
)

py_binary(
    name = "inverted_pendulum",
    srcs = ["inverted_pendulum.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//examples/vpython:vpython_stub",
        "@pip//numpy",
    ],
)

py_binary(
    name = "sliding_pendulum",
    srcs = ["sliding_pendulum.py"],
    visibility = ["//:__subpackages__"],
    deps = ["//examples/vpython:vpython_stub"],
)
