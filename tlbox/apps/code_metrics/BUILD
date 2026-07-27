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
        "@toolbox_pip//click",
        "@toolbox_pip//psycopg2_binary",
        "@toolbox_pip//sqlalchemy",
        "@toolbox_pip//tabulate",
    ],
)

py_binary(
    name = "models",
    srcs = ["models.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@toolbox_pip//psycopg2_binary",
        "@toolbox_pip//sqlalchemy",
    ],
)
