package(default_visibility = ["//visibility:private"])

filegroup(
    name = "component_images",
    srcs = glob(["*.png"]),
)

filegroup(
    name = "docs",
    srcs = [
        "sbr_components.md",
        ":component_images",
    ],
    visibility = ["//docs:__pkg__"],
)
