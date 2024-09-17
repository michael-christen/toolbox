load("//bzl:py.bzl", "py_library")
load("//tools/sphinx:sphinx.bzl", "sphinx_html")

filegroup(
    name = "templates",
    srcs = glob(["_templates/**/*.rst"]),
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
        # "myst_extensions.md",
        "examples.md",
        "//:python_source",
        ":templates",
        ":static",
    ],
    config = "conf.py",
    index = "index.rst",  # Test non-canonical naming.
)

package(default_visibility = ["//visibility:private"])
