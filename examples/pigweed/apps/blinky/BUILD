load("@pigweed//targets/host_device_simulator:transition.bzl", "host_device_simulator_binary")
load("//bzl:cc.bzl", "cc_binary")
load("//third_party/pigweed/tools:tools.bzl", "host_console")

package(default_visibility = ["//visibility:private"])

cc_binary(
    name = "blinky",
    srcs = ["main.cc"],
    deps = [
        "//examples/pigweed/apps/blinky/system:headers",
        "//examples/pigweed/modules/blinky:service",
        "//third_party/pigweed:pw_system_async_alias",
        "@pigweed//pw_async2:system_time_provider",
        "@pigweed//pw_log",
    ],
)

# Create a host binary using the Pigweed upstream pw_system host_device_simulator.
host_device_simulator_binary(
    name = "simulator_blinky",
    binary = ":blinky",
)

host_console(
    name = "simulator_console",
    binary = ":simulator_blinky",
)

host_console(
    name = "simulator_webconsole",
    binary = ":simulator_blinky",
    extra_args = ["--browser"],
)
