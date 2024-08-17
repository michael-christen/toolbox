load("@pigweed//targets/host_device_simulator:transition.bzl", "host_device_simulator_binary")
load("//examples/pigweed/tools:tools.bzl", "host_console")

package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "blinky",
    srcs = ["main.cc"],
    deps = [
        "//examples/pigweed/modules/blinky:service",
        "//system",
        "@pigweed//pw_log",
        "@pigweed//pw_system:async",

        # These should be provided by pw_system:async.
        "@pigweed//pw_assert:assert_backend_impl",
        "@pigweed//pw_assert:check_backend_impl",
        "@pigweed//pw_log:backend_impl",
        "@pigweed//pw_system:extra_platform_libs",
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
