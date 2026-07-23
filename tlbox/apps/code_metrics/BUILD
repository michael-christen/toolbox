load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "main",
    srcs = ["main.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        ":models",
        "//tlbox/utils:bazel_utils",
        "//tlbox/utils:git_utils",
        "@pip//click",
        "@pip//psycopg2_binary",
        "@pip//sqlalchemy",
        "@pip//tabulate",
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
