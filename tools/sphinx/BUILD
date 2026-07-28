load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "sphinx_build_wrapper",
    srcs = ["sphinx_build_wrapper.py"],
    tags = ["no-mypy"],
    visibility = ["//visibility:public"],
    deps = [
        "@toolbox_pip//furo",  # keep
        "@toolbox_pip//linkify_it_py",  # keep
        "@toolbox_pip//myst_parser",  # keep
        "@toolbox_pip//sphinx",  # keep
        "@toolbox_pip//sphinx_autoapi",  # keep
        "@toolbox_pip//sphinx_copybutton",  # keep
        "@toolbox_pip//sphinx_design",  # keep
        "@toolbox_pip//sphinx_pyscript",  # keep
        "@toolbox_pip//sphinx_rtd_theme",  # keep
        "@toolbox_pip//sphinx_tippy",  # keep
        "@toolbox_pip//sphinx_togglebutton",  # keep
        "@toolbox_pip//sphinxcontrib_mermaid",  # keep
        "@toolbox_pip//sphinxext_opengraph",  # keep
        "@toolbox_pip//sphinxext_rediraffe",  # keep
    ],
)
