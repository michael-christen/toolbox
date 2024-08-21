import sphinx_rtd_theme

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'toolbox'
copyright = '2024, Michael Christen'
author = 'Michael Christen'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
    "myst_parser",
    "sphinxcontrib.mermaid",
    "autoapi.extension",
]
autoapi_dirs = [
    # "./",
    "../",
    "../examples",
    # "../examples/basic",
    # "../examples/bazel",
]
autoapi_type = "python"
# Maybe set to True (need to show directory structure though)
# XXX:
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_python_use_implicit_namespaces
# - configure toctree to find these properly now
autoapi_python_use_implicit_namespaces = True

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
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

exclude_patterns = []

# `root_doc`: Provided at Bazel level


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
templates_path = ['_templates']

# html_sidebars = {
#     "**": [
#         "navigation.html",
#     ],
# }
