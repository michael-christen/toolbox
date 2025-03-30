load("//bzl:py.bzl", "py_binary", "py_library")

package(default_visibility = ["//visibility:private"])

filegroup(
    name = "python_source",
    srcs = glob(["*.py"]) + [
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "bazel_parser",
    srcs = ["bazel_parser.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        ":panel",
        "//third_party/bazel/src/main/protobuf:build_py_library",
        "//tools:bazel_utils",
        "//tools:git_py_library",
        "//tools:git_utils",
        "//utils:bep_reader",
        "//utils:graph_algorithms",
        "@pip//click",
        "@pip//networkx",
        # XXX: Should associate with networkx
        "@pip//pygraphviz",  # keep
    ],
)

py_library(
    name = "panel",
    srcs = ["panel.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip//bokeh",
        "@pip//networkx",
        "@pip//panel",
    ],
    tags = [
        # Bokeh type-hinting is raising a lot of complaints that are invalid
        "no-mypy",
    ],
)
