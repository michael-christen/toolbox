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
        "hello.rst",
        "myst.md",
        # has warnings
        "myst_extensions.md",
        "examples.md",
        "bringup.md",
        "useful_commands.md",
        "//:python_source",
        ":templates",
        ":img",
        ":static",
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
