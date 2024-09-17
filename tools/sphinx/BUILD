load("//bzl:py.bzl", "py_binary")

py_binary(
    name = "sphinx_build_wrapper",
    srcs = ["sphinx_build_wrapper.py"],
    visibility = ["//visibility:public"],
    deps = ["@pip//sphinx",
            "@pip//sphinx_rtd_theme",
            "@pip//myst_parser",
            "@pip//sphinxcontrib_mermaid",
            "@pip//sphinx_autoapi",
    ],
)

package(default_visibility = ["//visibility:private"])
