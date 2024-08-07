load("//bzl:cc.bzl", "cc_library")


# Alternatively, we could just use @catch2//:catch_main
cc_library(
    name = "catch_main",
    testonly=True,
    srcs = ["catch_main.cc"],
    deps = [
        "@catch2",
    ],
    visibility = ["//visibility:public"],
)
