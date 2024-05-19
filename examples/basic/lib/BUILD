load("@rules_cc//cc:defs.bzl", "cc_library")

cc_library(
    name = "hello-time",
    srcs = ["hello-time.cc"],
    hdrs = ["hello-time.h"],
    visibility = ["//examples/basic/app:__pkg__"],
    deps = [
        # "@com_google_protobuf//:protobuf",
        "//external:protobuf",
    ],
)

package(default_visibility = ["//visibility:private"])
