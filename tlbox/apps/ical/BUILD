load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "read_ical_rrules",
    srcs = ["read_ical_rrules.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//icalendar"],
)
