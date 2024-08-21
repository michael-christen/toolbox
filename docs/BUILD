load("//tools/sphinx:sphinx.bzl", "sphinx_html")

sphinx_html(
    name = "docs",
    config = "conf.py",
    index = "index.rst",  # Test non-canonical naming.
    srcs = [
        "hello.rst",
        "myst.md",
        # has warnings
        # "myst_extensions.md",
        "examples.md",
        "example.py",
        "//:python_source",
    ],

)
