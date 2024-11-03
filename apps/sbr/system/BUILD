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
