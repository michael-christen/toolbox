load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "sphinx_build_wrapper",
    srcs = ["sphinx_build_wrapper.py"],
    visibility = ["//visibility:public"],
    deps = [
        "@pip//linkify_it_py",  # keep
        "@pip//myst_parser",  # keep
        "@pip//sphinx",  # keep
        "@pip//sphinx_autoapi",  # keep
        "@pip//sphinx_rtd_theme",  # keep
        "@pip//sphinxcontrib_mermaid",  # keep
    ],
)
