load("//bzl:py.bzl", "py_library")
load("//tools/sphinx:sphinx.bzl", "sphinx_html")

package(default_visibility = ["//visibility:private"])

filegroup(
    name = "templates",
    srcs = glob(["_templates/**/*.rst"]),
)

filegroup(
    name = "img",
    srcs = glob(["img/**"]),
)

filegroup(
    name = "static",
    srcs = glob(["_static/**/*.png"]),
)

sphinx_html(
    name = "docs",
    srcs = [
        "README.md",
        "bringup.md",
        "common_references.md",
        "examples.md",
        "myst.md",
        "myst_extensions.md",
        "useful_commands.md",
        ":img",
        ":static",
        ":templates",
        "//:python_source",
        "//docs/common:docs",
    ],
    config = "conf.py",
    index = "index.rst",  # Test non-canonical naming.
    # args = ["--keep-going", "--fail-on-warning"],
)

py_library(
    name = "conf",
    srcs = ["conf.py"],
    tags = ["no-mypy"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//sphinx_rtd_theme"],
)
