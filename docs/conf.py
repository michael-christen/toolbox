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
    # "sphinx_autoapi",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinxext.rediraffe",
    "sphinxext.opengraph",
    "sphinx_pyscript",
    "sphinx_tippy",
    "sphinx_togglebutton",
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


def setup(app):
    """Add functions to the Sphinx setup."""
    # from myst_parser._docs import (
    #     DirectiveDoc,
    #     DocutilsCliHelpDirective,
    #     MystAdmonitionDirective,
    #     MystConfigDirective,
    #     MystExampleDirective,
    #     MystLexer,
    #     MystToHTMLDirective,
    #     MystWarningsDirective,
    #     NumberSections,
    #     StripUnsupportedLatex,
    # )

    # app.add_directive("myst-config", MystConfigDirective)
    # app.add_directive("docutils-cli-help", DocutilsCliHelpDirective)
    # app.add_directive("doc-directive", DirectiveDoc)
    # app.add_directive("myst-warnings", MystWarningsDirective)
    # app.add_directive("myst-example", MystExampleDirective)
    # app.add_directive("myst-admonitions", MystAdmonitionDirective)
    # app.add_directive("myst-to-html", MystToHTMLDirective)
    # app.add_post_transform(StripUnsupportedLatex)
    # app.add_post_transform(NumberSections)
    # app.add_lexer("myst", MystLexer)

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

html_theme = "sphinx_rtd_theme"
# html_theme = "sphinx_book_theme"
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

suppress_warnings = [
    # Only supported in html
    "myst.strikethrough",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.10", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
    "markdown_it": ("https://markdown-it-py.readthedocs.io/en/latest", None),
}

rediraffe_redirects = {
}
