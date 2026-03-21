load("@pigweed//pw_build:compatibility.bzl", "host_backend_alias", "incompatible_with_mcu")
load("@rules_cc//cc:cc_library.bzl", "cc_library")

# gazelle:default_visibility //visibility:public
# gazelle:cc_group_unit_cycles warn
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
        "@pigweed//pw_i2c:register_device",  # keep
    ],
)

cc_library(
    name = "host_system",
    srcs = [
        "host_system.cc",
    ],
    implementation_deps = [
        "//platforms/host:initiator_host",
        "//third_party/pigweed/system:common_host_system",
        "@pigweed//pw_i2c:address",  # keep
        "@pigweed//pw_i2c:register_device",  # keep
        "@pigweed//pw_system:async",  # keep
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
        "@pigweed//pw_i2c:address",  # keep
        "@pigweed//pw_i2c:register_device",  # keep
        "@pigweed//pw_i2c_rp2040",  # keep
    ],
    deps = [
        "//apps/sbr/system:headers",
        "//hw_drivers/lis3mdl",
        "//third_party/pigweed/system:common_rp2_system",
    ],
)
