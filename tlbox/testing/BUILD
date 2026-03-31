load("//bzl:cc.bzl", "cc_library")

# gazelle:ignore
package(default_visibility = ["//visibility:private"])

# Wraps @googletest//:gtest_main so tests depend on //tlbox/testing:gtest_main,
# giving us a place to add custom setup/teardown hooks if needed.
cc_library(
    name = "gtest_main",
    testonly = True,
    visibility = ["//visibility:public"],
    deps = [
        "@googletest//:gtest_main",
    ],
)

# pw_log_string handler for pw_cc_test targets.
#
# pw_system:log_backend (the default) routes PW_LOG_* into a MultiSink drained
# by the RPC stack, which never starts in tests. This handler writes directly to
# pw_sys_io (stdio on host) so PW_LOG output appears in test output.
#
# Wired up via .bazelrc:
#   --@pigweed//pw_log_string:handler_backend=//tlbox/testing:log_string_handler
cc_library(
    name = "log_string_handler",
    srcs = ["log_string_handler.cc"],
    visibility = ["//visibility:public"],
    deps = [
        "@pigweed//pw_string:builder",
        "@pigweed//pw_sys_io",
    ],
)
