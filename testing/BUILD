load("//bzl:cc.bzl", "cc_library")

# Alternatively, we could just use @catch2//:catch_main
cc_library(
    name = "catch_main",
    testonly = True,
    srcs = ["catch_main.cc"],
    visibility = ["//visibility:public"],
    deps = [
        "@catch2",
    ],
)

package(default_visibility = ["//visibility:private"])
