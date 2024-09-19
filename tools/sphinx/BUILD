load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "sphinx_build_wrapper",
    srcs = ["sphinx_build_wrapper.py"],
    tags = ["no-mypy"],
    visibility = ["//visibility:public"],
    deps = [
        "@pip//linkify_it_py",  # keep
        "@pip//myst_parser",  # keep
        "@pip//sphinx",  # keep
        "@pip//sphinx_autoapi",  # keep
        "@pip//sphinx_book_theme",  # keep
        "@pip//sphinx_copybutton",  # keep
        "@pip//sphinx_design",  # keep
        "@pip//sphinx_pyscript",  # keep
        "@pip//sphinx_rtd_theme",  # keep
        "@pip//sphinx_tippy",  # keep
        "@pip//sphinx_togglebutton",  # keep
        "@pip//sphinxcontrib_mermaid",  # keep
        "@pip//sphinxext_opengraph",  # keep
        "@pip//sphinxext_rediraffe",  # keep
    ],
)
