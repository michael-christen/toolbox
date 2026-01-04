load("@pigweed//targets/host_device_simulator:transition.bzl", "host_device_simulator_binary")
load("@pigweed//targets/rp2040:flash.bzl", "flash_rp2040")
load("@rules_cc//cc:cc_binary.bzl", "cc_binary")
load("//bzl:cc.bzl", "cc_size")
load("//third_party/pigweed/tools:tools.bzl", "device_console", "host_console")
load(":binary.bzl", "rp2040_binary", "rp2350_binary")

package(default_visibility = ["//visibility:private"])

cc_binary(
    name = "sbr",
    srcs = ["main.cc"],
    deps = [
        "//apps/sbr/system",
        "//hw_services/sbr:service",
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

cc_size(
    # XXX: 100 and 100 are wrong ...
    max_flash = 100,
    max_ram = 100,
    target = ":rp2040_sbr.elf",
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

cc_size(
    # XXX: 100 and 100 are wrong ...
    max_flash = 100,
    max_ram = 100,
    target = ":rp2350_sbr.elf",
)

# Note: Despite the name, the rule works for the 2350.
flash_rp2040(
    name = "flash_rp2350",
    rp2040_binary = "rp2350_sbr.elf",
)
