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
)

cc_library(
    name = "host_system",
    srcs = [
        "host_system.cc",
    ],
    implementation_deps = [
        "//third_party/pigweed/system:common_host_system",
        "@pigweed//pw_system:async",
    ],
    target_compatible_with = incompatible_with_mcu(),
    deps = ["//apps/sbr/system:headers"],
)

cc_library(
    name = "rp2_system",
    srcs = [
        "rp2_system.cc",
    ],
    deps = [
        "//apps/sbr/system:headers",
        "//third_party/pigweed/system:common_rp2_system",
    ],
)
