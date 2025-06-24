load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "car_tutorial",
    srcs = ["car_tutorial.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//simpy"],
)

py_binary(
    name = "thermostat_example",
    srcs = ["thermostat_example.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//simpy"],
)
