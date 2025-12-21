load("//bzl:py.bzl", "py_binary")

py_binary(
    name = "tutorial",
    srcs = ["tutorial.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//sqlalchemy"],
)

package(default_visibility = ["//visibility:private"])
