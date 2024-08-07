load("//bzl:cc.bzl", "cc_library", "cc_binary")

package(default_visibility = ["//visibility:private"])

cc_library(
    name = "hello-greet",
    srcs = ["hello-greet.cc"],
    hdrs = ["hello-greet.h"],
)

cc_binary(
    name = "hello-world",
    srcs = ["hello-world.cc"],
    deps = [
        ":hello-greet",
        "//examples/basic:hello_cc_library",
        "//examples/basic/lib:hello-time",
    ],
)
