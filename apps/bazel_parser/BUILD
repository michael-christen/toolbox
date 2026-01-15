load("//bzl:py.bzl", "py_binary", "py_image", "py_library", "py_test")

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
        ":repo_graph_data",
        "@pip//numpy",
        "@pip//pandas",
    ],
)

py_library(
    name = "repo_graph_data",
    srcs = ["repo_graph_data.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "//utils:graph_algorithms",
        "@pip//networkx",
        "@pip//pandas",
        "@pip//tqdm",
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
        "//tools:git_utils",
        "@pip//networkx",
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
        "//tools:bazel_utils",
        "//tools:git_py_library",
        "//tools:git_utils",
        "//utils:bep_reader",
        "@pip//click",
        "@pip//networkx",
        "@pip//pydantic",
        # XXX: Should associate with networkx
        "@pip//pygraphviz",  # keep
        "@pip//pyyaml",
    ],
)

# XXX: This still requires that folks bring their own python runtime
# py_pex_binary(
#     name = "cli_pex",
#     binary = ":cli",
# )

# XXX: Need to mount volume and bazel is not found, etc
# Build and run this image with
#     bazel run //apps/bazel_parser:bazel_parser_img_load_docker
#     docker run --rm bazel_parser:latest
py_image(
    name = "bazel_parser_img",
    binary = ":cli",
    image_tags = ["bazel_parser:latest"],
)
