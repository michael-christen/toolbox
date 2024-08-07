load("//bzl:cc.bzl", "cc_library", "cc_test")

package(default_visibility = ["//visibility:private"])

cc_library(
    name = "hello-time",
    srcs = ["hello-time.cc"],
    hdrs = ["hello-time.h"],
    visibility = ["//examples/basic/app:__pkg__"],
)

cc_test(
    name = "hello_test",
    srcs = ["hello_test.cc"],
    deps = [
        # Alternatively, we could depend on @catch2//:catch_main
        "//testing:catch_main",
    ],
)
