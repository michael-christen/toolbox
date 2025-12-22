load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "tutorial",
    srcs = ["tutorial.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//sqlalchemy"],
)
