load("@rules_cc//cc:defs.bzl", "cc_library")

cc_library(
    name = "hello-time",
    srcs = ["hello-time.cc"],
    hdrs = ["hello-time.h"],
    deps = [
        # "@com_google_protobuf//:protobuf",
        "//external:protobuf",
    ],
    visibility = ["//examples/basic/app:__pkg__"],
)

package(default_visibility = ["//visibility:private"])
