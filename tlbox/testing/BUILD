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
