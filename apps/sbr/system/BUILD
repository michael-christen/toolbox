load("@pigweed//pw_build:compatibility.bzl", "host_backend_alias", "incompatible_with_mcu")

# gazelle:default_visibility //visibility:public
package(default_visibility = ["//visibility:public"])

label_flag(
    name = "system",
    build_setting_default = ":unspecified_backend",
)

host_backend_alias(
    name = "unspecified_backend",
    backend = ":host_system",
)

cc_library(
    name = "headers",
    hdrs = [
        "system.h",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "@pigweed//pw_i2c:register_device",
    ],
)

cc_library(
    name = "host_system",
    srcs = [
        "host_system.cc",
    ],
    implementation_deps = [
        "@pigweed//pw_i2c:address",
        "@pigweed//pw_i2c:register_device",
        # XXX: Build out different kinds of fakes
        "//platforms/host:initiator_host",
        "@pigweed//pw_channel",
        "@pigweed//pw_channel:stream_channel",
        "@pigweed//pw_digital_io",
        "@pigweed//pw_digital_io:digital_io_mock",
        "@pigweed//pw_multibuf:simple_allocator",
        "@pigweed//pw_system:async",
        "@pigweed//pw_system:io",
    ],
    target_compatible_with = incompatible_with_mcu(),
    deps = ["//apps/sbr/system:headers"],
)

cc_library(
    name = "rp2_system",
    srcs = [
        "rp2_system.cc",
    ],
    implementation_deps = [
        "@pico-sdk//src/rp2_common/cmsis:cmsis_core",
        "@pico-sdk//src/rp2_common/hardware_adc",
        "@pico-sdk//src/rp2_common/hardware_exception:hardware_exception",
        "@pico-sdk//src/rp2_common/pico_stdlib:pico_stdlib",
        "@pigweed//pw_channel",
        "@pigweed//pw_channel:rp2_stdio_channel",
        "@pigweed//pw_cpu_exception:entry_backend_impl",
        "@pigweed//pw_digital_io",
        "@pigweed//pw_digital_io:digital_io_mock",
        "@pigweed//pw_digital_io_rp2040",
        "@pigweed//pw_i2c:address",
        "@pigweed//pw_i2c:register_device",
        "@pigweed//pw_i2c_rp2040",
        "@pigweed//pw_multibuf:simple_allocator",
        "@pigweed//pw_system:async",
        "@pigweed//pw_system:io",
        "@pigweed//third_party/freertos:support",
    ],
    deps = ["//apps/sbr/system:headers"],
)
