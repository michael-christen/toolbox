load("@pigweed//targets/host_device_simulator:transition.bzl", "host_device_simulator_binary")
load("@pigweed//targets/rp2040:flash.bzl", "flash_rp2040")

load(":binary.bzl", "rp2040_binary", "rp2350_binary")
load("//examples/pigweed/tools:tools.bzl", "host_console", "device_console")

package(default_visibility = ["//visibility:private"])

cc_binary(
    name = "sbr",
    srcs = ["main.cc"],
    deps = [
        "//apps/sbr/system",
        "//hw_service/sbr:service",
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
    name = "simulator_sbr",
    binary = ":sbr",
)

host_console(
    name = "simulator_console",
    binary = ":simulator_sbr",
)

host_console(
    name = "simulator_webconsole",
    binary = ":simulator_sbr",
    extra_args = ["--browser"],
)

# Create an rp2040 flashable ELF
rp2040_binary(
    name = "rp2040_sbr.elf",
    binary = ":sbr",
)

flash_rp2040(
    name = "flash_rp2040",
    rp2040_binary = "rp2040_sbr.elf",
)

device_console(
    name = "rp2040_console",
    binary = ":rp2040_sbr.elf",
)


# Create an rp2350 flashable ELF
rp2350_binary(
    name = "rp2350_sbr.elf",
    binary = ":sbr",
)

# Note: Despite the name, the rule works for the 2350.
flash_rp2040(
    name = "flash_rp2350",
    rp2040_binary = "rp2350_sbr.elf",
)
