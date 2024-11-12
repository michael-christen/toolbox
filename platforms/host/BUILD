package(default_visibility = ["//visibility:private"])

cc_library(
    name = "initiator_host",
    srcs = ["initiator_host.cc"],
    hdrs = ["initiator_host.h"],
    visibility = ["//apps/sbr/system:__pkg__"],
    deps = [
        "@pigweed//pw_i2c:address",
        "@pigweed//pw_i2c:initiator",
    ],
)
