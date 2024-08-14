load("@pigweed//targets/host_device_simulator:transition.bzl", "host_device_simulator_binary")
load("@pigweed//targets/rp2040:flash.bzl", "flash_rp2040")
# load("//targets/rp2:binary.bzl", "rp2040_binary", "rp2350_binary")

package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "blinky",
    srcs = ["main.cc"],
    deps = [
        # "//modules/blinky:service",
        # "//modules/board:service",
        # "//system:worker",
        # "//system",
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

# # Create an rp2040 flashable ELF
# rp2040_binary(
#     name = "rp2040_blinky.elf",
#     binary = ":blinky",
# )

# # Create an rp2350 flashable ELF
# rp2350_binary(
#     name = "rp2350_blinky.elf",
#     binary = ":blinky",
# )

# sense_host_console(
#     name = "simulator_console",
#     binary = ":simulator_blinky",
# )
# 
# sense_host_console(
#     name = "simulator_webconsole",
#     binary = ":simulator_blinky",
#     extra_args = ["--browser"],
# )
# 
# sense_device_console(
#     name = "rp2040_console",
#     binary = ":rp2040_blinky.elf",
# )
# 
# sense_device_console(
#     name = "rp2040_webconsole",
#     binary = ":rp2040_blinky.elf",
#     extra_args = ["--browser"],
# )
# 
# sense_device_console(
#     name = "rp2350_console",
#     binary = ":rp2350_blinky.elf",
# )
# 
# sense_device_console(
#     name = "rp2350_webconsole",
#     binary = ":rp2350_blinky.elf",
#     extra_args = ["--browser"],
# )
# 
# sense_device_script(
#     name = "rp2040_example_script",
#     src = "//tools:example_script",
#     binary = ":rp2040_blinky.elf",
# )
# 
# sense_device_script(
#     name = "rp2350_example_script",
#     src = "//tools:example_script",
#     binary = ":rp2350_blinky.elf",
# )
# 
# sense_device_script(
#     name = "rp2040_toggle_blinky",
#     src = "//tools:toggle_blinky",
#     binary = ":rp2040_blinky.elf",
# )
# 
# sense_device_script(
#     name = "rp2350_toggle_blinky",
#     src = "//tools:toggle_blinky",
#     binary = ":rp2350_blinky.elf",
# )
# 
# alias(
#     name = "flash",
#     actual = ":flash_rp2040",
# )
# 
# flash_rp2040(
#     name = "flash_rp2040",
#     rp2040_binary = "rp2040_blinky.elf",
# )
# 
# # Note: Despite the name, the rule works for the 2350.
# flash_rp2040(
#     name = "flash_rp2350",
#     rp2040_binary = "rp2350_blinky.elf",
# )
