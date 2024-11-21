load("@pip//:requirements.bzl", "all_requirements")
load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "ipython",
    srcs = ["ipython.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip//ipython",
        "//tools:git_utils",  # keep
    ] + all_requirements,  # keep
)
