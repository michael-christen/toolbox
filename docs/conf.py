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
    "autoapi.extension",
]
autoapi_dirs = [
    # XXX: Would be nice to not have to add
    "../examples",
    # XXX: Not showing apps
    "../apps",
]
autoapi_type = "python"
autoapi_template_dir = "_templates/autoapi"
# Maybe set to True (need to show directory structure though)
# XXX:
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_python_use_implicit_namespaces
# - configure toctree to find these properly now
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
# XXX: Maybe just signature
autodoc_typehints = "both"


def skip_member(app, what, name, obj, skip, options):
    # XXX: conditional breakpoint here
    return skip


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_member)


myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    # "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

exclude_patterns = []

# `root_doc`: Provided at Bazel level


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
# html_theme = 'furo'

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
