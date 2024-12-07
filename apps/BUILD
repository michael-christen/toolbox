load("//bzl:py.bzl", "py_binary")

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
        "//third_party/bazel/src/main/protobuf:build_py_library",
        "//tools:bazel_utils",
        "//tools:git_utils",
        "//utils:bep_reader",
        "//utils:graph_algorithms",
        "@pip//bokeh",
        "@pip//networkx",
        # XXX: Should associate with networkx
        "@pip//pygraphviz",  # keep
        "@pip//panel",
    ],
)

# XXX: Example case of py_binary conflicting
py_binary(
    name = "example_bokeh",
    srcs = ["example_bokeh.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip//bokeh",
        "@pip//networkx",
        "@pip//panel",
        # XXX: I needed to install system clang to build the wheel, I likely
        # should point elsewhere for hermeticity
        # XXX: Should associate with networkx
        "@pip//pygraphviz",  # keep
    ],
)
