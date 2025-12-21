load("@pigweed//pw_build:compatibility.bzl", "incompatible_with_mcu")
load("@rules_cc//cc:cc_library.bzl", "cc_library")

package(default_visibility = ["//visibility:public"])

cc_library(
    name = "common_host_system",
    srcs = [
        "common_host_system.cc",
    ],
    hdrs = [
        "common_host_system.h",
    ],
    target_compatible_with = incompatible_with_mcu(),
    visibility = ["//visibility:public"],
    deps = [
        "@pigweed//pw_channel",
        "@pigweed//pw_channel:stream_channel",
        "@pigweed//pw_digital_io",
        "@pigweed//pw_digital_io:digital_io_mock",
        "@pigweed//pw_multibuf:simple_allocator",
        "@pigweed//pw_system:async",
        "@pigweed//pw_system:io",
    ],
)

cc_library(
    name = "common_rp2_system",
    srcs = [
        "common_rp2_system.cc",
    ],
    hdrs = [
        "common_rp2_system.h",
    ],
    implementation_deps = [
        "@pico-sdk//src/rp2_common/cmsis:cmsis_core",
        "@pico-sdk//src/rp2_common/hardware_adc",
        "@pico-sdk//src/rp2_common/hardware_exception:hardware_exception",
        "@pico-sdk//src/rp2_common/pico_stdlib:pico_stdlib",
        "@pigweed//pw_channel",
        "@pigweed//pw_cpu_exception:entry_backend_impl",
        "@pigweed//pw_digital_io",
        "@pigweed//pw_digital_io:digital_io_mock",
        "@pigweed//pw_digital_io_rp2040",
        "@pigweed//third_party/freertos:support",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "@pigweed//pw_channel:rp2_stdio_channel",
        "@pigweed//pw_multibuf:simple_allocator",
        "@pigweed//pw_system:async",
        "@pigweed//pw_system:io",
    ],
)
