load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "main",
    srcs = ["main.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        ":models",
        "//tools:bazel_utils",
        "//tools:git_utils",
        "@pip//psycopg2_binary",
        "@pip//sqlalchemy",
    ],
)

py_binary(
    name = "models",
    srcs = ["models.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip//psycopg2_binary",
        "@pip//sqlalchemy",
    ],
)
