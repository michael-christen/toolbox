load("//bzl:py.bzl", "py_library")
load("//tools/sphinx:sphinx.bzl", "sphinx_html")

filegroup(
    name = "templates",
    srcs = glob(["_templates/**/*.rst"]),
)

sphinx_html(
    name = "docs",
    srcs = [
        "hello.rst",
        "myst.md",
        # has warnings
        # "myst_extensions.md",
        "examples.md",
        "//:python_source",
        ":templates",
    ],
    config = "conf.py",
    index = "index.rst",  # Test non-canonical naming.
)

package(default_visibility = ["//visibility:private"])

py_library(
    name = "conf",
    srcs = ["conf.py"],
    visibility = ["//:__subpackages__"],
)
