load("//bzl:py.bzl", "py_binary")

py_binary(
    name = "tofupilot_example",
    srcs = ["tofupilot_example.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip//openhtf",
        "@pip//tofupilot",
        "@pip//six",  # keep
    ],
)

package(default_visibility = ["//visibility:private"])
