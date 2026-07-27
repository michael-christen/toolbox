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
        "@toolbox_pip//bokeh",
        "@toolbox_pip//networkx",
        "@toolbox_pip//panel",
    ],
)

py_library(
    name = "refinement",
    srcs = ["refinement.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        ":repo_graph_data",
        "@toolbox_pip//numpy",
        "@toolbox_pip//pandas",
    ],
)

py_library(
    name = "repo_graph_data",
    srcs = ["repo_graph_data.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//tlbox/utils:graph_algorithms",
        "@toolbox_pip//networkx",
        "@toolbox_pip//pandas",
        "@toolbox_pip//tqdm",
    ],
)

py_test(
    name = "repo_graph_data_test",
    srcs = ["repo_graph_data_test.py"],
    deps = [
        ":repo_graph_data",
        "@toolbox_pip//networkx",
    ],
)

py_library(
    name = "parsing",
    srcs = ["parsing.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        ":repo_graph_data",
        "//third_party/bazel/src/main/protobuf:build_py_library",
        "//tlbox/utils:git_utils",
        "@toolbox_pip//networkx",
    ],
)

py_binary(
    name = "cli",
    srcs = ["cli.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        ":panel",
        ":parsing",
        ":refinement",
        "//tlbox/utils:bazel_utils",
        "//tlbox/utils:bep_reader",
        "//tlbox/utils:git_utils",
        "//tools:git_py_library",
        "@toolbox_pip//click",
        "@toolbox_pip//networkx",
        "@toolbox_pip//pandas",
        "@toolbox_pip//pydantic",
        "@toolbox_pip//pyyaml",
    ],
)
