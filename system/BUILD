load("@pigweed//pw_build:compatibility.bzl", "host_backend_alias")

# gazelle:default_visibility //visibility:public
package(default_visibility = ["//visibility:public"])

cc_library(
    name = "module_config",
    defines = [
        # TODO: https://pwbug.dev/352389854 - Move this to per-platform config
        # when platform flags  are implemented.
        #
        # Allow us to capture two 64bit pointers in a pw::function.
        "PW_FUNCTION_INLINE_CALLABLE_SIZE=16UL",
        "PW_ASSERT_BASIC_ACTION=PW_ASSERT_BASIC_ACTION_EXIT",
    ],
    visibility = ["//visibility:public"],
)

label_flag(
    name = "system",
    build_setting_default = ":unspecified_backend",
)

host_backend_alias(
    name = "unspecified_backend",
    backend = "//examples/pigweed/targets/host:system",
)

cc_library(
    name = "headers",
    hdrs = [
        "system.h",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "@pigweed//pw_digital_io",
    ],
)
