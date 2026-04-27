load("//bzl:py.bzl", "py_binary", "py_test")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "scheduler",
    srcs = ["scheduler.py"],
    deps = ["@pip//anthropic"],
)

py_test(
    name = "scheduler_test",
    srcs = ["scheduler_test.py"],
    deps = [
        ":scheduler",
        "@pip//anthropic",
    ],
)
