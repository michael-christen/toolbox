# Keep things easy for now
# gazelle:default_visibility //visibility:public
load("//bzl:cc.bzl", "cc_library")

package(default_visibility = ["//visibility:public"])

filegroup(
    name = "pw_console_config",
    srcs = [
        ".pw_console.yaml",
    ],
    visibility = ["//visibility:public"],
)


# Work around gazelle limitations
cc_library(
    name = "pw_system_async_alias",
    deps = [
        "@pigweed//pw_assert:assert_backend_impl",
        "@pigweed//pw_assert:check_backend_impl",
        "@pigweed//pw_log:backend_impl",
        "@pigweed//pw_system:extra_platform_libs",
        "@pigweed//pw_system:async",
    ],
)
