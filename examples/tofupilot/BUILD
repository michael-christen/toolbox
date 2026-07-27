load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "tofupilot_example",
    srcs = ["tofupilot_example.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@toolbox_pip//openhtf",
        "@toolbox_pip//tofupilot",
    ],
)
