# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sphinx_rtd_theme  # noqa

project = "toolbox"
copyright = "2024, Michael Christen"
author = "Michael Christen"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "autoapi.extension",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinxext.rediraffe",
    "sphinxext.opengraph",
    "sphinx_pyscript",
    "sphinx_tippy",
    "sphinx_togglebutton",
]
autoapi_dirs = [
    "../examples",
    "../apps",
]
autoapi_type = "python"
autoapi_template_dir = "_templates/autoapi"
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_python_use_implicit_namespaces
autoapi_python_use_implicit_namespaces = True
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_options
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
# Keep outputs around for debugging
autoapi_keep_files = True
# signature, description, both, none: are the options
# MAYBE: just signature
autodoc_typehints = "both"


def skip_member(app, what, name, obj, skip, options):
    # NOTE, if curious can add conditional breakpoint here
    return skip


def setup(app):
    """Add functions to the Sphinx setup."""
    app.connect("autoapi-skip-member", skip_member)


myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "attrs_block",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
myst_heading_anchors = 3

exclude_patterns = []

# `root_doc`: Provided at Bazel level

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"

html_static_path = ["_static"]
# html_logo = "_static/wrench.png"
html_favicon = "_static/wrench.png"
# html_theme_options = {
#     "logo_only": True,
#     "display_version": False,
# }
# html_sidebars = {
#     "**": [
#         "navigation.html",
#     ],
# }
templates_path = ["_templates"]

suppress_warnings = [
    # Only supported in html
    "myst.strikethrough",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.10", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
    "markdown_it": ("https://markdown-it-py.readthedocs.io/en/latest", None),
}

rediraffe_redirects = {}
