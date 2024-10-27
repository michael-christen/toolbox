load("@com_google_emboss//:build_defs.bzl", "emboss_cc_library")
load("//bzl:cc.bzl", "cc_library", "cc_test")

emboss_cc_library(
    name = "lis3mdl_emb",
    srcs = ["lis3mdl.emb"],
)

cc_library(
    name = "lis3mdl",
    srcs = ["lis3mdl.cc"],
    hdrs = ["lis3mdl.h"],
    deps = [
        ":lis3mdl_emb",
    ],
)


cc_test(
    name = "lis3mdl_test",
    srcs = ["lis3mdl_test.cc"],
    deps = [
        ":lis3mdl_emb",
        "//testing:catch_main",
    ],
)
