selector_to_html = {"a[href=\"README.html#language-faqs\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Language FAQs<a class=\"headerlink\" href=\"#language-faqs\" title=\"Link to this heading\">\uf0c1</a></h2><p>Generally, each language needs a way to answer these questions:</p>", "a[href=\"examples.html#heres-another-section\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Here\u2019s another section<a class=\"headerlink\" href=\"#heres-another-section\" title=\"Link to this heading\">\uf0c1</a></h2><p>And some more content.</p><p><a class=\"reference internal\" href=\"#section-two\"><span class=\"std std-ref\">a reference to this section</span></a>. I can also reference the\nsection <a class=\"reference internal\" href=\"#section-two\"><span class=\"std std-ref\">Here\u2019s another section</span></a> without specifying my title.</p>", "a[href=\"README.html#adding-modifying-external-dependencies\"]": "<h4 class=\"tippy-header\" style=\"margin-top: 0;\">Adding / Modifying External Dependencies<a class=\"headerlink\" href=\"#adding-modifying-external-dependencies\" title=\"Link to this heading\">\uf0c1</a></h4><p>NOTE: Once <code class=\"docutils literal notranslate\"><span class=\"pre\">requirements.in</span></code> is modified, tests will ensure the above commands\nhave been run (or CI will fail)</p>", "a[href=\"myst_extensions.html#linkify\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Linkify<a class=\"headerlink\" href=\"#linkify\" title=\"Link to this heading\">\uf0c1</a></h2><p>Adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"linkify\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>) will automatically identify \u201cbare\u201d web URLs and add hyperlinks:</p><p><code class=\"docutils literal notranslate\"><span class=\"pre\">www.example.com</span></code> -&gt; <a class=\"reference external\" href=\"http://www.example.com\">www.example.com</a></p>", "a[href=\"README.html#notes\"]": "<h4 class=\"tippy-header\" style=\"margin-top: 0;\">Notes<a class=\"headerlink\" href=\"#notes\" title=\"Link to this heading\">\uf0c1</a></h4>", "a[href=\"README.html#miscellaneous\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Miscellaneous<a class=\"headerlink\" href=\"#miscellaneous\" title=\"Link to this heading\">\uf0c1</a></h3><h4>Bazel Options<a class=\"headerlink\" href=\"#bazel-options\" title=\"Link to this heading\">\uf0c1</a></h4>", "a[href=\"useful_commands.html#package-commands\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Package Commands<a class=\"headerlink\" href=\"#package-commands\" title=\"Link to this heading\">\uf0c1</a></h3><p>Get package dependencies:</p>", "a[href=\"README.html#bazel-options\"]": "<h4 class=\"tippy-header\" style=\"margin-top: 0;\">Bazel Options<a class=\"headerlink\" href=\"#bazel-options\" title=\"Link to this heading\">\uf0c1</a></h4>", "a[href=\"README.html#get-tsan-to-work-on-ubuntu-24-04\"]": "<h4 class=\"tippy-header\" style=\"margin-top: 0;\">Get tsan to work on Ubuntu 24.04<a class=\"headerlink\" href=\"#get-tsan-to-work-on-ubuntu-24-04\" title=\"Link to this heading\">\uf0c1</a></h4><p><a class=\"reference external\" href=\"https://stackoverflow.com/a/77856955\">https://stackoverflow.com/a/77856955</a></p>", "a[href=\"README.html#excluding-coverage\"]": "<h4 class=\"tippy-header\" style=\"margin-top: 0;\">Excluding coverage<a class=\"headerlink\" href=\"#excluding-coverage\" title=\"Link to this heading\">\uf0c1</a></h4><p><code class=\"docutils literal notranslate\"><span class=\"pre\">#</span> <span class=\"pre\">pragma:</span> <span class=\"pre\">no</span> <span class=\"pre\">cover</span></code> <a class=\"reference external\" href=\"https://coverage.readthedocs.io/en/latest/excluding.html\">https://coverage.readthedocs.io/en/latest/excluding.html</a></p>", "a[href=\"myst_extensions.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Syntax Extensions<a class=\"headerlink\" href=\"#syntax-extensions\" title=\"Link to this heading\">\uf0c1</a></h1><p>The following syntaxes are optional (disabled by default) and can be enabled\n<em>via</em> the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code> (see also\n<a class=\"reference external\" href=\"https://myst-parser.readthedocs.io/en/latest/configuration.html#sphinx-config-options\">Configuration</a>).\nTheir goal is generally to add more <em>Markdown friendly</em> syntaxes; often enabling\nand rendering markdown-it-py plugins that extend the\n<a class=\"reference external\" href=\"https://commonmark.org/\">CommonMark specification</a>.</p><p>To enable all the syntaxes explained below:</p>", "a[href=\"myst_extensions.html#code-fences-using-colons\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Code fences using colons<a class=\"headerlink\" href=\"#code-fences-using-colons\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"colon_fence\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou can also use <code class=\"docutils literal notranslate\"><span class=\"pre\">:::</span></code> delimiters to denote directives, instead of <code class=\"docutils literal notranslate\"><span class=\"pre\">```</span></code>.</p><p>Using colons instead of back-ticks has the benefit of allowing the content to be rendered correctly, when you are working in any standard Markdown editor.\nIt is ideal for admonition type directives (as documented in Directives) or tables with titles, for example:</p>", "a[href=\"myst_extensions.html#math-in-other-block-elements\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Math in other block elements<a class=\"headerlink\" href=\"#math-in-other-block-elements\" title=\"Link to this heading\">\uf0c1</a></h3><p>Math will also work when nested in other block elements, like lists or quotes:</p>", "a[href=\"autoapi/apps/bazel_parser/index.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">apps.bazel_parser<a class=\"headerlink\" href=\"#module-apps.bazel_parser\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"useful_commands.html#bash\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Bash<a class=\"headerlink\" href=\"#bash\" title=\"Link to this heading\">\uf0c1</a></h2><h3>Argument shortcuts<a class=\"headerlink\" href=\"#argument-shortcuts\" title=\"Link to this heading\">\uf0c1</a></h3><p><a class=\"reference external\" href=\"https://stackoverflow.com/questions/4009412/how-to-use-arguments-from-previous-command\">https://stackoverflow.com/questions/4009412/how-to-use-arguments-from-previous-command</a></p>", "a[href=\"myst_extensions.html#inline-attributes\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Inline attributes<a class=\"headerlink\" href=\"#inline-attributes\" title=\"Link to this heading\">\uf0c1</a></h3><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"attrs_inline\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou can enable parsing of inline attributes after certain inline syntaxes.</p><p>For example, the following Markdown:</p>", "a[href=\"myst_extensions.html#substitutions-with-jinja2\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Substitutions (with Jinja2)<a class=\"headerlink\" href=\"#substitutions-with-jinja2\" title=\"Link to this heading\">\uf0c1</a></h2><p>Adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"substitution\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>) will allow you to add substitutions, added in either the <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code> using <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_substitutions</span></code>:</p>", "a[href=\"myst_extensions.html#markdown-figures\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Markdown Figures<a class=\"headerlink\" href=\"#markdown-figures\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"colon_fence\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nwe can combine the above two extended syntaxes,\nto create a fully Markdown compliant version of the <code class=\"docutils literal notranslate\"><span class=\"pre\">figure</span></code> directive named <code class=\"docutils literal notranslate\"><span class=\"pre\">figure-md</span></code>.</p>", "a[href=\"README.html#c\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">C++<a class=\"headerlink\" href=\"#c\" title=\"Link to this heading\">\uf0c1</a></h3><p>Testing utilizes <a class=\"reference external\" href=\"https://github.com/catchorg/Catch2\">catch2</a></p>", "a[href=\"#toolbox-documentation\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">toolbox documentation<a class=\"headerlink\" href=\"#toolbox-documentation\" title=\"Link to this heading\">\uf0c1</a></h1><p>Add your content using <code class=\"docutils literal notranslate\"><span class=\"pre\">reStructuredText</span></code> syntax. See the\n<a class=\"reference external\" href=\"https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html\">reStructuredText</a>\ndocumentation for details.</p>", "a[href=\"myst_extensions.html#anchor-slug-structure\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Anchor slug structure<a class=\"headerlink\" href=\"#anchor-slug-structure\" title=\"Link to this heading\">\uf0c1</a></h3><p>The anchor \u201cslugs\u201d created aim to follow the <a class=\"reference external\" href=\"https://github.com/Flet/github-slugger\">GitHub implementation</a>:</p>", "a[href=\"myst_extensions.html#html-images\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">HTML Images<a class=\"headerlink\" href=\"#html-images\" title=\"Link to this heading\">\uf0c1</a></h2><p>MyST provides a few different syntaxes for including images in your documentation, as explained below.</p><p>The first is the standard Markdown syntax:</p>", "a[href=\"bringup.html#log\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Log<a class=\"headerlink\" href=\"#log\" title=\"Link to this heading\">\uf0c1</a></h2><p>2023-12-27, Wednesday:</p>", "a[href=\"common/python_references.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Python References<a class=\"headerlink\" href=\"#python-references\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Strings<a class=\"headerlink\" href=\"#strings\" title=\"Link to this heading\">\uf0c1</a></h2><p><a class=\"reference external\" href=\"https://docs.python.org/3/library/string.html#format-specification-mini-language\">https://docs.python.org/3/library/string.html#format-specification-mini-language</a></p>", "a[href=\"myst_extensions.html#substitutions-and-urls\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Substitutions and URLs<a class=\"headerlink\" href=\"#substitutions-and-urls\" title=\"Link to this heading\">\uf0c1</a></h3><p>Substitutions cannot be directly used in URLs, such as <code class=\"docutils literal notranslate\"><span class=\"pre\">[a</span> <span class=\"pre\">link](https://{{key4}}.com)</span></code> or <code class=\"docutils literal notranslate\"><span class=\"pre\">&lt;https://{{key4}}.com&gt;</span></code>.\nHowever, since Jinja2 substitutions allow for Python methods to be used, you can use string formatting or replacements:</p>", "a[href=\"README.html#badges\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Badges<a class=\"headerlink\" href=\"#badges\" title=\"Link to this heading\">\uf0c1</a></h2><p><a class=\"reference external\" href=\"https://codecov.io/gh/michael-christen/toolbox\"><img alt=\"codecov\" src=\"https://codecov.io/gh/michael-christen/toolbox/graph/badge.svg?token=GGS6QHC5YP\"/></a></p><p>NOTE: Our coverage setup doesn\u2019t find completely uncovered files. We\u2019ll need to\nfix that at some point, for now be aware of it.</p>", "a[href=\"myst_extensions.html#attributes\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Attributes<a class=\"headerlink\" href=\"#attributes\" title=\"Link to this heading\">\uf0c1</a></h2><p>Attributes are a way of enriching standard CommonMark syntax, by adding additional information to elements.</p><p>Attributes are specified inside curly braces <code class=\"docutils literal notranslate\"><span class=\"pre\">{}</span></code>,\nfor example <code class=\"docutils literal notranslate\"><span class=\"pre\">{#my-id</span> <span class=\"pre\">.my-class</span> <span class=\"pre\">key=\"value\"}</span></code>,\nand come before a block element or after an inline element.</p>", "a[href=\"common/python_references.html#strings\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Strings<a class=\"headerlink\" href=\"#strings\" title=\"Link to this heading\">\uf0c1</a></h2><p><a class=\"reference external\" href=\"https://docs.python.org/3/library/string.html#format-specification-mini-language\">https://docs.python.org/3/library/string.html#format-specification-mini-language</a></p>", "a[href=\"myst_extensions.html#inspect-the-links-that-will-be-created\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Inspect the links that will be created<a class=\"headerlink\" href=\"#inspect-the-links-that-will-be-created\" title=\"Link to this heading\">\uf0c1</a></h3><p>You can inspect the links that will be created using the command-line tool:</p>", "a[href=\"README.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">toolbox<a class=\"headerlink\" href=\"#toolbox\" title=\"Link to this heading\">\uf0c1</a></h1><p>My personal monorepo.</p><p>Find <a class=\"reference external\" href=\"https://michael-christen.github.io/toolbox\">docs here</a></p>", "a[href=\"myst.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">MyST<a class=\"headerlink\" href=\"#myst\" title=\"Link to this heading\">\uf0c1</a></h1><p>Great news, we don\u2019t have to use .rst, we can leverage\n<a class=\"reference external\" href=\"https://mystmd.org/\">MyST</a> to write markdown.</p><p>MyST makes Markdown more <em>extensible</em> &amp; <strong>powerful</strong> to support an ecosystem of\ntools for computational narratives, technical documentation, and open scientific\ncommunication.</p>", "a[href=\"README.html#id1\"]": "<h4 class=\"tippy-header\" style=\"margin-top: 0;\">Command Quick Reference<a class=\"headerlink\" href=\"#id1\" title=\"Link to this heading\">\uf0c1</a></h4><p>Copied from \u201cBazel\u201d</p>", "a[href=\"myst_extensions.html#direct-latex-math\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Direct LaTeX Math<a class=\"headerlink\" href=\"#direct-latex-math\" title=\"Link to this heading\">\uf0c1</a></h3><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"amsmath\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou can enable direct parsing of <a class=\"reference external\" href=\"https://ctan.org/pkg/amsmath\">amsmath</a> LaTeX equations.\nThese top-level math environments will then be directly parsed:</p>", "a[href=\"README.html#installation-instructions\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Installation Instructions<a class=\"headerlink\" href=\"#installation-instructions\" title=\"Link to this heading\">\uf0c1</a></h3>", "a[href=\"myst_extensions.html#definition-lists\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Definition Lists<a class=\"headerlink\" href=\"#definition-lists\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"deflist\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou will be able to utilise definition lists.\nDefinition lists utilise the , which itself is based on the <a class=\"reference external\" href=\"http://johnmacfarlane.net/pandoc/README.html#definition-lists\">Pandoc definition list specification</a>.</p><p>This syntax can be useful, for example, as an alternative to nested bullet-lists:</p>", "a[href=\"useful_commands.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Useful Commands<a class=\"headerlink\" href=\"#useful-commands\" title=\"Link to this heading\">\uf0c1</a></h1><p>This is just a place for me to put small commands that I find myself looking up\nfrequently.</p>", "a[href=\"useful_commands.html#argument-shortcuts\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Argument shortcuts<a class=\"headerlink\" href=\"#argument-shortcuts\" title=\"Link to this heading\">\uf0c1</a></h3><p><a class=\"reference external\" href=\"https://stackoverflow.com/questions/4009412/how-to-use-arguments-from-previous-command\">https://stackoverflow.com/questions/4009412/how-to-use-arguments-from-previous-command</a></p>", "a[href=\"README.html#references\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">References<a class=\"headerlink\" href=\"#references\" title=\"Link to this heading\">\uf0c1</a></h2><h3>Bazel<a class=\"headerlink\" href=\"#bazel\" title=\"Link to this heading\">\uf0c1</a></h3><h4>Command Quick Reference<a class=\"headerlink\" href=\"#command-quick-reference\" title=\"Link to this heading\">\uf0c1</a></h4><p>NOTE: this doesn\u2019t seem to be working \u2026</p>", "a[href=\"myst_extensions.html#admonition-directives\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Admonition directives<a class=\"headerlink\" href=\"#admonition-directives\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"README.html#todo\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">TODO<a class=\"headerlink\" href=\"#todo\" title=\"Link to this heading\">\uf0c1</a></h2><h3>CI<a class=\"headerlink\" href=\"#ci\" title=\"Link to this heading\">\uf0c1</a></h3>", "a[href=\"myst_extensions.html#auto-generated-header-anchors\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Auto-generated header anchors<a class=\"headerlink\" href=\"#auto-generated-header-anchors\" title=\"Link to this heading\">\uf0c1</a></h2><p>The MyST Parser can automatically generate label \u201cslugs\u201d for header anchors so that you can reference them from markdown links.\nFor example, you can use header bookmark links, locally; <code class=\"docutils literal notranslate\"><span class=\"pre\">[](#header-anchor)</span></code>, or cross-file <code class=\"docutils literal notranslate\"><span class=\"pre\">[](path/to/file.md#header-anchor)</span></code>.\nTo achieve this, use the <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_heading_anchors</span> <span class=\"pre\">=</span> <span class=\"pre\">DEPTH</span></code> configuration option, where <code class=\"docutils literal notranslate\"><span class=\"pre\">DEPTH</span></code> is the depth of header levels for which you wish to generate links.</p><p>For example, the following configuration in <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code> tells the <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_parser</span></code> to generate labels for heading anchors for <code class=\"docutils literal notranslate\"><span class=\"pre\">h1</span></code>, <code class=\"docutils literal notranslate\"><span class=\"pre\">h2</span></code>, and <code class=\"docutils literal notranslate\"><span class=\"pre\">h3</span></code> level headings (corresponding to <code class=\"docutils literal notranslate\"><span class=\"pre\">#</span></code>, <code class=\"docutils literal notranslate\"><span class=\"pre\">##</span></code>, and <code class=\"docutils literal notranslate\"><span class=\"pre\">###</span></code> in markdown).</p>", "a[href=\"README.html#command-quick-reference\"]": "<h4 class=\"tippy-header\" style=\"margin-top: 0;\">Command Quick Reference<a class=\"headerlink\" href=\"#command-quick-reference\" title=\"Link to this heading\">\uf0c1</a></h4><p>NOTE: this doesn\u2019t seem to be working \u2026</p>", "a[href=\"README.html#rust\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Rust<a class=\"headerlink\" href=\"#rust\" title=\"Link to this heading\">\uf0c1</a></h3><h4>Command Quick Reference<a class=\"headerlink\" href=\"#id1\" title=\"Link to this heading\">\uf0c1</a></h4><p>Copied from \u201cBazel\u201d</p>", "a[href=\"README.html#inspiration\"]": "<h4 class=\"tippy-header\" style=\"margin-top: 0;\">Inspiration<a class=\"headerlink\" href=\"#inspiration\" title=\"Link to this heading\">\uf0c1</a></h4>", "a[href=\"bringup.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Log for How I am Bringing up This Repo and My New Server<a class=\"headerlink\" href=\"#log-for-how-i-am-bringing-up-this-repo-and-my-new-server\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Log<a class=\"headerlink\" href=\"#log\" title=\"Link to this heading\">\uf0c1</a></h2><p>2023-12-27, Wednesday:</p>", "a[href=\"README.html#python\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Python<a class=\"headerlink\" href=\"#python\" title=\"Link to this heading\">\uf0c1</a></h3><h4>Excluding coverage<a class=\"headerlink\" href=\"#excluding-coverage\" title=\"Link to this heading\">\uf0c1</a></h4><p><code class=\"docutils literal notranslate\"><span class=\"pre\">#</span> <span class=\"pre\">pragma:</span> <span class=\"pre\">no</span> <span class=\"pre\">cover</span></code> <a class=\"reference external\" href=\"https://coverage.readthedocs.io/en/latest/excluding.html\">https://coverage.readthedocs.io/en/latest/excluding.html</a></p>", "a[href=\"myst_extensions.html#html-admonitions\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">HTML Admonitions<a class=\"headerlink\" href=\"#html-admonitions\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"html_admonition\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou can enable parsing of <code class=\"docutils literal notranslate\"><span class=\"pre\">&lt;div</span> <span class=\"pre\">class=\"admonition\"&gt;</span></code> HTML blocks.\nThese blocks will be converted internally to Sphinx admonition directives, and so will work correctly for all output formats.\nThis is helpful when you care about viewing the \u201csource\u201d Markdown, such as in Jupyter Notebooks.</p><p>If the first element within the <code class=\"docutils literal notranslate\"><span class=\"pre\">div</span></code> is <code class=\"docutils literal notranslate\"><span class=\"pre\">&lt;div</span> <span class=\"pre\">class=\"title\"&gt;</span></code> or <code class=\"docutils literal notranslate\"><span class=\"pre\">&lt;p</span> <span class=\"pre\">class=\"title\"&gt;</span></code>, then this will be set as the admonition title.\nAll internal text (and the title) will be parsed as MyST-Markdown and all classes and an optional name will be passed to the admonition:</p>", "a[href=\"myst_extensions.html#mathjax-and-math-parsing\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Mathjax and math parsing<a class=\"headerlink\" href=\"#mathjax-and-math-parsing\" title=\"Link to this heading\">\uf0c1</a></h3><p>When building HTML using the  extension (enabled by default),\nIf <code class=\"docutils literal notranslate\"><span class=\"pre\">dollarmath</span></code> is enabled, Myst-Parser injects the <code class=\"docutils literal notranslate\"><span class=\"pre\">tex2jax_ignore</span></code> (MathJax v2) and  <code class=\"docutils literal notranslate\"><span class=\"pre\">mathjax_ignore</span></code> (MathJax v3) classes in to the top-level section of each MyST document, and adds the following default MathJax configuration:</p><p>MathJax version 2 (see <a class=\"reference external\" href=\"https://docs.mathjax.org/en/v2.7-latest/options/preprocessors/tex2jax.html#configure-tex2jax\">the tex2jax preprocessor</a>:</p>", "a[href=\"README.html#getting-started\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Getting Started<a class=\"headerlink\" href=\"#getting-started\" title=\"Link to this heading\">\uf0c1</a></h3>", "a[href=\"README.html#layout\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Layout<a class=\"headerlink\" href=\"#layout\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"myst_extensions.html#task-lists\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Task Lists<a class=\"headerlink\" href=\"#task-lists\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"tasklist\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou will be able to utilise task lists.\nTask lists utilise the ,\nand are applied to markdown list items starting with <code class=\"docutils literal notranslate\"><span class=\"pre\">[</span> <span class=\"pre\">]</span></code> or <code class=\"docutils literal notranslate\"><span class=\"pre\">[x]</span></code>:</p>", "a[href=\"myst_extensions.html#field-lists\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Field Lists<a class=\"headerlink\" href=\"#field-lists\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"fieldlist\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou will be able to utilise field lists.\nField lists are mappings from field names to field bodies,\nbased on the <a class=\"reference external\" href=\"https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#field-lists\">reStructureText syntax</a>.</p>", "a[href=\"myst_extensions.html#math-shortcuts\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Math shortcuts<a class=\"headerlink\" href=\"#math-shortcuts\" title=\"Link to this heading\">\uf0c1</a></h2><p>Math is parsed by adding to the <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> list option, in the\nsphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code> one or both of:</p>", "a[href=\"README.html#bazel\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Bazel<a class=\"headerlink\" href=\"#bazel\" title=\"Link to this heading\">\uf0c1</a></h3><h4>Command Quick Reference<a class=\"headerlink\" href=\"#command-quick-reference\" title=\"Link to this heading\">\uf0c1</a></h4><p>NOTE: this doesn\u2019t seem to be working \u2026</p>", "a[href=\"README.html#ci\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">CI<a class=\"headerlink\" href=\"#ci\" title=\"Link to this heading\">\uf0c1</a></h3>", "a[href=\"common_references.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Common References<a class=\"headerlink\" href=\"#common-references\" title=\"Link to this heading\">\uf0c1</a></h1><p>Common references that are often used.</p>", "a[href=\"useful_commands.html#reload-udev-rules\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Reload udev rules:<a class=\"headerlink\" href=\"#reload-udev-rules\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"myst_extensions.html#block-attributes\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Block attributes<a class=\"headerlink\" href=\"#block-attributes\" title=\"Link to this heading\">\uf0c1</a></h3><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"attrs_block\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou can enable parsing of block attributes before certain block syntaxes.</p><p>For example, the following Markdown:</p>", "a[href=\"README.html#configuration-tools-used\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Configuration / Tools Used<a class=\"headerlink\" href=\"#configuration-tools-used\" title=\"Link to this heading\">\uf0c1</a></h2><p>This section describes how the various tools are setup and used in the repo.</p>", "a[href=\"autoapi/index.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">API Reference<a class=\"headerlink\" href=\"#api-reference\" title=\"Link to this heading\">\uf0c1</a></h1><p>This page contains auto-generated API reference documentation <a class=\"footnote-reference brackets\" href=\"#f1\" id=\"id1\" role=\"doc-noteref\"><span class=\"fn-bracket\">[</span>1<span class=\"fn-bracket\">]</span></a>.</p>", "a[href=\"examples.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">My nifty title<a class=\"headerlink\" href=\"#my-nifty-title\" title=\"Link to this heading\">\uf0c1</a></h1><p>Some <strong>text</strong>!</p>", "a[href=\"myst_extensions.html#send_message\"]": "<dt class=\"sig sig-object py\" id=\"send_message\">\n<span class=\"sig-name descname\"><span class=\"pre\">send_message</span></span><span class=\"sig-paren\">(</span><em class=\"sig-param\"><span class=\"n\"><span class=\"pre\">sender</span></span></em>, <em class=\"sig-param\"><span class=\"n\"><span class=\"pre\">priority</span></span></em><span class=\"sig-paren\">)</span></dt><dd><p>Send a message to a recipient</p></dd>"}
skip_classes = ["headerlink", "sd-stretched-link"]

window.onload = function () {
    for (const [select, tip_html] of Object.entries(selector_to_html)) {
        const links = document.querySelectorAll(` ${select}`);
        for (const link of links) {
            if (skip_classes.some(c => link.classList.contains(c))) {
                continue;
            }

            tippy(link, {
                content: tip_html,
                allowHTML: true,
                arrow: true,
                placement: 'auto-start', maxWidth: 500, interactive: false,

            });
        };
    };
    console.log("tippy tips loaded!");
};
