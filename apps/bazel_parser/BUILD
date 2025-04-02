load("//bzl:py.bzl", "py_binary", "py_library", "py_test")

package(default_visibility = ["//visibility:private"])

filegroup(
    name = "python_source",
    srcs = glob(["*.py"]) + [
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "panel",
    srcs = ["panel.py"],
    tags = [
        # Bokeh type-hinting is raising a lot of complaints that are invalid
        "no-mypy",
    ],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip//bokeh",
        "@pip//networkx",
        "@pip//panel",
    ],
)

py_library(
    name = "refinement",
    srcs = ["refinement.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip//networkx",
        "@pip//numpy",
        "@pip//pandas",
    ],
)

py_library(
    name = "repo_graph_data",
    srcs = ["repo_graph_data.py"],
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
        "@pip//pandas",
    ],
)

py_test(
    name = "repo_graph_data_test",
    srcs = ["repo_graph_data_test.py"],
    deps = [
        ":repo_graph_data",
        "@pip//networkx",
    ],
)

py_library(
    name = "parsing",
    srcs = ["parsing.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        ":repo_graph_data",
        "//third_party/bazel/src/main/protobuf:build_py_library",
        "//tools:bazel_utils",
        "//tools:git_py_library",
        "//tools:git_utils",
        "//utils:bep_reader",
        "//utils:graph_algorithms",
        "@pip//click",
        "@pip//networkx",
        "@pip//pandas",
    ],
)

py_binary(
    name = "cli",
    srcs = ["cli.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        ":panel",
        ":parsing",
        ":repo_graph_data",
        "//third_party/bazel/src/main/protobuf:build_py_library",
        "//tools:bazel_utils",
        "//tools:git_py_library",
        "//tools:git_utils",
        "//utils:bep_reader",
        "//utils:graph_algorithms",
        "@pip//click",
        "@pip//networkx",
        "@pip//pandas",
        # XXX: Should associate with networkx
        "@pip//pygraphviz",  # keep
    ],
)
