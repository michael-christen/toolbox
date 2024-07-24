
load("@bazel_skylib//rules:native_binary.bzl", "native_binary")
# XXX: load("@pigweed//pw_system/py:console.bzl", "device_console", "device_simulator_console")
# XXX: load("@pigweed//targets/host_device_simulator:transition.bzl", "host_device_simulator_binary")
load("//targets:transition.bzl", "rp2040_binary", "stm32_binary")

package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "blinky",
    srcs = ["main.cc"],
    deps = [
        "//libraries/pw_board_led",
        "@pigweed//pw_chrono:system_clock",
        "@pigweed//pw_chrono:system_timer",
        "@pigweed//pw_log",
        "@pigweed//pw_system",
    ],
)

stm32_binary(
    name = "stm32_blinky.elf",
    binary = ":blinky",
)

rp2040_binary(
    name = "rp2040_blinky.elf",
    binary = ":blinky",
)

# native_binary(
#     name = "flash_stm32",
#     src = "//tools:flash_device",
#     args = [
#         "--device",
#         "STM32-Discovery",
#         "$(rootpath //examples/01_blinky:stm32_blinky.elf)",
#     ],
#     data = [":stm32_blinky.elf"],
# )

# XXX: device_console(
# XXX:     name = "console_stm32",
# XXX:     binary = ":stm32_blinky.elf",
# XXX:     pw_console_config = "//:pw_console_config",
# XXX:     script = "//tools:console",
# XXX: )
# XXX: 
# XXX: device_console(
# XXX:     name = "console_rp2040",
# XXX:     binary = ":rp2040_blinky.elf",
# XXX:     pw_console_config = "//:pw_console_config",
# XXX:     script = "//tools:console",
# XXX: )

# Create a host binary using the Pigweed upstream pw_system host_device_simulator.
# XXX: host_device_simulator_binary(
# XXX:     name = "simulator_blinky",
# XXX:     binary = ":blinky",
# XXX: )

# Start :simulator_blinky and connect to it with pw console by running:
#   bazel run //examples/01_blinky:simulator_console
# XXX: device_simulator_console(
# XXX:     name = "simulator_console",
# XXX:     host_binary = ":simulator_blinky",
# XXX:     pw_console_config = "//:pw_console_config",
# XXX:     script = "//tools:device_sim",
# XXX: )
