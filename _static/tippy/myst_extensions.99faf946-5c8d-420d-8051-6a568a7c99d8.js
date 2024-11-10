selector_to_html = {"a[href=\"#substitutions-and-urls\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Substitutions and URLs<a class=\"headerlink\" href=\"#substitutions-and-urls\" title=\"Link to this heading\">\uf0c1</a></h3><p>Substitutions cannot be directly used in URLs, such as <code class=\"docutils literal notranslate\"><span class=\"pre\">[a</span> <span class=\"pre\">link](https://{{key4}}.com)</span></code> or <code class=\"docutils literal notranslate\"><span class=\"pre\">&lt;https://{{key4}}.com&gt;</span></code>.\nHowever, since Jinja2 substitutions allow for Python methods to be used, you can use string formatting or replacements:</p>", "a[href=\"#admonition-directives\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Admonition directives<a class=\"headerlink\" href=\"#admonition-directives\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#field-lists\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Field Lists<a class=\"headerlink\" href=\"#field-lists\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"fieldlist\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou will be able to utilise field lists.\nField lists are mappings from field names to field bodies,\nbased on the <a class=\"reference external\" href=\"https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#field-lists\">reStructureText syntax</a>.</p>", "a[href=\"#syntax-attributes\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Attributes<a class=\"headerlink\" href=\"#attributes\" title=\"Link to this heading\">\uf0c1</a></h2><p>Attributes are a way of enriching standard CommonMark syntax, by adding additional information to elements.</p><p>Attributes are specified inside curly braces <code class=\"docutils literal notranslate\"><span class=\"pre\">{}</span></code>,\nfor example <code class=\"docutils literal notranslate\"><span class=\"pre\">{#my-id</span> <span class=\"pre\">.my-class</span> <span class=\"pre\">key=\"value\"}</span></code>,\nand come before a block element or after an inline element.</p>", "a[href=\"#equation-f323db9b-a6b4-4d39-bb7d-55c8800f1c82\"]": "<div class=\"amsmath math notranslate nohighlight\" id=\"equation-f323db9b-a6b4-4d39-bb7d-55c8800f1c82\">\n\\[\\begin{align}\na_{11}&amp; =b_{11}&amp;\n  a_{12}&amp; =b_{12}\\\\\na_{21}&amp; =b_{21}&amp;\n  a_{22}&amp; =b_{22}+c_{22}\n\\end{align}\\]</div>", "a[href=\"#code-fences-using-colons\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Code fences using colons<a class=\"headerlink\" href=\"#code-fences-using-colons\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"colon_fence\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou can also use <code class=\"docutils literal notranslate\"><span class=\"pre\">:::</span></code> delimiters to denote directives, instead of <code class=\"docutils literal notranslate\"><span class=\"pre\">```</span></code>.</p><p>Using colons instead of back-ticks has the benefit of allowing the content to be rendered correctly, when you are working in any standard Markdown editor.\nIt is ideal for admonition type directives (as documented in Directives) or tables with titles, for example:</p>", "a[href=\"#equation-eqn-best\"]": "<div class=\"math notranslate nohighlight\" id=\"equation-eqn-best\">\n\\[\ne = mc^2\n\\]</div>", "a[href=\"#attributes\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Attributes<a class=\"headerlink\" href=\"#attributes\" title=\"Link to this heading\">\uf0c1</a></h2><p>Attributes are a way of enriching standard CommonMark syntax, by adding additional information to elements.</p><p>Attributes are specified inside curly braces <code class=\"docutils literal notranslate\"><span class=\"pre\">{}</span></code>,\nfor example <code class=\"docutils literal notranslate\"><span class=\"pre\">{#my-id</span> <span class=\"pre\">.my-class</span> <span class=\"pre\">key=\"value\"}</span></code>,\nand come before a block element or after an inline element.</p>", "a[href=\"#math-in-other-block-elements\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Math in other block elements<a class=\"headerlink\" href=\"#math-in-other-block-elements\" title=\"Link to this heading\">\uf0c1</a></h3><p>Math will also work when nested in other block elements, like lists or quotes:</p>", "a[href=\"#anchor-slug-structure\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Anchor slug structure<a class=\"headerlink\" href=\"#anchor-slug-structure\" title=\"Link to this heading\">\uf0c1</a></h3><p>The anchor \u201cslugs\u201d created aim to follow the <a class=\"reference external\" href=\"https://github.com/Flet/github-slugger\">GitHub implementation</a>:</p>", "a[href=\"#markdown-figures\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Markdown Figures<a class=\"headerlink\" href=\"#markdown-figures\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"colon_fence\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nwe can combine the above two extended syntaxes,\nto create a fully Markdown compliant version of the <code class=\"docutils literal notranslate\"><span class=\"pre\">figure</span></code> directive named <code class=\"docutils literal notranslate\"><span class=\"pre\">figure-md</span></code>.</p>", "a[href=\"#block-attributes\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Block attributes<a class=\"headerlink\" href=\"#block-attributes\" title=\"Link to this heading\">\uf0c1</a></h3><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"attrs_block\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou can enable parsing of block attributes before certain block syntaxes.</p><p>For example, the following Markdown:</p>", "a[href=\"#mathjax-and-math-parsing\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Mathjax and math parsing<a class=\"headerlink\" href=\"#mathjax-and-math-parsing\" title=\"Link to this heading\">\uf0c1</a></h3><p>When building HTML using the <a class=\"reference external\" href=\"https://www.sphinx-doc.org/en/master/usage/extensions/math.html#module-sphinx.ext.mathjax\" title=\"Sphinx 8.2.0\"><code class=\"docutils literal notranslate\"><span class=\"pre\">sphinx.ext.mathjax</span></code></a> extension (enabled by default),\nIf <code class=\"docutils literal notranslate\"><span class=\"pre\">dollarmath</span></code> is enabled, Myst-Parser injects the <code class=\"docutils literal notranslate\"><span class=\"pre\">tex2jax_ignore</span></code> (MathJax v2) and  <code class=\"docutils literal notranslate\"><span class=\"pre\">mathjax_ignore</span></code> (MathJax v3) classes in to the top-level section of each MyST document, and adds the following default MathJax configuration:</p><p>MathJax version 2 (see <a class=\"reference external\" href=\"https://docs.mathjax.org/en/v2.7-latest/options/preprocessors/tex2jax.html#configure-tex2jax\">the tex2jax preprocessor</a>:</p>", "a[href=\"#syntax-definition-lists\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Definition Lists<a class=\"headerlink\" href=\"#definition-lists\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"deflist\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou will be able to utilise definition lists.\nDefinition lists utilise the <a class=\"reference external\" href=\"https://markdown-it-py.readthedocs.io/en/latest/plugins.html#md-plugins\" title=\"markdown-it-py\">markdown-it-py deflist plugin</a>, which itself is based on the <a class=\"reference external\" href=\"http://johnmacfarlane.net/pandoc/README.html#definition-lists\">Pandoc definition list specification</a>.</p><p>This syntax can be useful, for example, as an alternative to nested bullet-lists:</p>", "a[href=\"#auto-generated-header-anchors\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Auto-generated header anchors<a class=\"headerlink\" href=\"#auto-generated-header-anchors\" title=\"Link to this heading\">\uf0c1</a></h2><p>The MyST Parser can automatically generate label \u201cslugs\u201d for header anchors so that you can reference them from markdown links.\nFor example, you can use header bookmark links, locally; <code class=\"docutils literal notranslate\"><span class=\"pre\">[](#header-anchor)</span></code>, or cross-file <code class=\"docutils literal notranslate\"><span class=\"pre\">[](path/to/file.md#header-anchor)</span></code>.\nTo achieve this, use the <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_heading_anchors</span> <span class=\"pre\">=</span> <span class=\"pre\">DEPTH</span></code> configuration option, where <code class=\"docutils literal notranslate\"><span class=\"pre\">DEPTH</span></code> is the depth of header levels for which you wish to generate links.</p><p>For example, the following configuration in <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code> tells the <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_parser</span></code> to generate labels for heading anchors for <code class=\"docutils literal notranslate\"><span class=\"pre\">h1</span></code>, <code class=\"docutils literal notranslate\"><span class=\"pre\">h2</span></code>, and <code class=\"docutils literal notranslate\"><span class=\"pre\">h3</span></code> level headings (corresponding to <code class=\"docutils literal notranslate\"><span class=\"pre\">#</span></code>, <code class=\"docutils literal notranslate\"><span class=\"pre\">##</span></code>, and <code class=\"docutils literal notranslate\"><span class=\"pre\">###</span></code> in markdown).</p>", "a[href=\"#direct-latex-math\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Direct LaTeX Math<a class=\"headerlink\" href=\"#direct-latex-math\" title=\"Link to this heading\">\uf0c1</a></h3><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"amsmath\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou can enable direct parsing of <a class=\"reference external\" href=\"https://ctan.org/pkg/amsmath\">amsmath</a> LaTeX equations.\nThese top-level math environments will then be directly parsed:</p>", "a[href=\"#term-term-name\"]": "<dt id=\"term-term-name\">term name</dt><dd><p>Definition of the term</p></dd>", "a[href=\"#mypara\"]": "<p class=\"bg-warning\" id=\"mypara\">Here is a paragraph with attributes.</p>", "a[href=\"#substitutions-with-jinja2\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Substitutions (with Jinja2)<a class=\"headerlink\" href=\"#substitutions-with-jinja2\" title=\"Link to this heading\">\uf0c1</a></h2><p>Adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"substitution\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>) will allow you to add substitutions, added in either the <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code> using <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_substitutions</span></code>:</p>", "a[href=\"#imgid\"]": "<img alt=\"An image with attribute\" class=\"bg-warning align-center\" id=\"imgid\" src=\"_images/fun-fish.png\" style=\"width: 100px;\"/>", "a[href=\"#send_message\"]": "<dt class=\"sig sig-object py\" id=\"send_message\">\n<span class=\"sig-name descname\"><span class=\"pre\">send_message</span></span><span class=\"sig-paren\">(</span><em class=\"sig-param\"><span class=\"n\"><span class=\"pre\">sender</span></span></em>, <em class=\"sig-param\"><span class=\"n\"><span class=\"pre\">priority</span></span></em><span class=\"sig-paren\">)</span></dt><dd><p>Send a message to a recipient</p></dd>", "a[href=\"#id3\"]": "<figure class=\"align-default\" id=\"id3\">\n<a class=\"bg-primary mb-1 reference internal image-reference\" href=\"_images/fun-fish.png\"><img alt=\"fishy\" class=\"bg-primary mb-1\" src=\"_images/fun-fish.png\" style=\"width: 200px;\"/>\n</a>\n<figcaption>\n<p><span class=\"caption-text\">This is a caption in <strong>Markdown</strong></span><a class=\"headerlink\" href=\"#id3\" title=\"Link to this image\">\uf0c1</a></p>\n</figcaption>\n</figure>", "a[href=\"#html-images\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">HTML Images<a class=\"headerlink\" href=\"#html-images\" title=\"Link to this heading\">\uf0c1</a></h2><p>MyST provides a few different syntaxes for including images in your documentation, as explained below.</p><p>The first is the standard Markdown syntax:</p>", "a[href=\"#inline-attributes\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Inline attributes<a class=\"headerlink\" href=\"#inline-attributes\" title=\"Link to this heading\">\uf0c1</a></h3><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"attrs_inline\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou can enable parsing of inline attributes after certain inline syntaxes.</p><p>For example, the following Markdown:</p>", "a[href=\"#inspect-the-links-that-will-be-created\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Inspect the links that will be created<a class=\"headerlink\" href=\"#inspect-the-links-that-will-be-created\" title=\"Link to this heading\">\uf0c1</a></h3><p>You can inspect the links that will be created using the command-line tool:</p>", "a[href=\"#linkify\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Linkify<a class=\"headerlink\" href=\"#linkify\" title=\"Link to this heading\">\uf0c1</a></h2><p>Adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"linkify\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>) will automatically identify \u201cbare\u201d web URLs and add hyperlinks:</p><p><code class=\"docutils literal notranslate\"><span class=\"pre\">www.example.com</span></code> -&gt; <a class=\"reference external\" href=\"http://www.example.com\">www.example.com</a></p>", "a[href=\"#definition-lists\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Definition Lists<a class=\"headerlink\" href=\"#definition-lists\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"deflist\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou will be able to utilise definition lists.\nDefinition lists utilise the <a class=\"reference external\" href=\"https://markdown-it-py.readthedocs.io/en/latest/plugins.html#md-plugins\" title=\"markdown-it-py\">markdown-it-py deflist plugin</a>, which itself is based on the <a class=\"reference external\" href=\"http://johnmacfarlane.net/pandoc/README.html#definition-lists\">Pandoc definition list specification</a>.</p><p>This syntax can be useful, for example, as an alternative to nested bullet-lists:</p>", "a[href=\"#task-lists\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Task Lists<a class=\"headerlink\" href=\"#task-lists\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"tasklist\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou will be able to utilise task lists.\nTask lists utilise the <a class=\"reference external\" href=\"https://markdown-it-py.readthedocs.io/en/latest/plugins.html#md-plugins\" title=\"markdown-it-py\">markdown-it-py tasklists plugin</a>,\nand are applied to markdown list items starting with <code class=\"docutils literal notranslate\"><span class=\"pre\">[</span> <span class=\"pre\">]</span></code> or <code class=\"docutils literal notranslate\"><span class=\"pre\">[x]</span></code>:</p>", "a[href=\"#id2\"]": "<table class=\"docutils align-center\" id=\"id2\">\n<caption><span class=\"caption-text\">This is a <strong>standard</strong> <em>Markdown</em> title</span><a class=\"headerlink\" href=\"#id2\" title=\"Link to this table\">\uf0c1</a></caption>\n<thead>\n<tr class=\"row-odd\"><th class=\"head\"><p>abc</p></th>\n<th class=\"head\"><p>mnp</p></th>\n<th class=\"head\"><p>xyz</p></th>\n</tr>\n</thead>\n<tbody>\n<tr class=\"row-even\"><td><p>123</p></td>\n<td><p>456</p></td>\n<td><p>789</p></td>\n</tr>\n</tbody>\n</table>", "a[href=\"#math-shortcuts\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Math shortcuts<a class=\"headerlink\" href=\"#math-shortcuts\" title=\"Link to this heading\">\uf0c1</a></h2><p>Math is parsed by adding to the <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> list option, in the\nsphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code> one or both of:</p>", "a[href=\"#fig-target\"]": "<figure class=\"myclass align-default\" id=\"fig-target\">\n<a class=\"bg-primary mb-1 reference internal image-reference\" href=\"_images/fun-fish.png\"><img alt=\"fishy\" class=\"bg-primary mb-1\" src=\"_images/fun-fish.png\" style=\"width: 200px;\"/>\n</a>\n<figcaption>\n<p><span class=\"caption-text\">This is a caption in <strong>Markdown</strong></span><a class=\"headerlink\" href=\"#fig-target\" title=\"Link to this image\">\uf0c1</a></p>\n</figcaption>\n</figure>", "a[href=\"#syntax-html-admonition\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">HTML Admonitions<a class=\"headerlink\" href=\"#html-admonitions\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"html_admonition\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou can enable parsing of <code class=\"docutils literal notranslate\"><span class=\"pre\">&lt;div</span> <span class=\"pre\">class=\"admonition\"&gt;</span></code> HTML blocks.\nThese blocks will be converted internally to Sphinx admonition directives, and so will work correctly for all output formats.\nThis is helpful when you care about viewing the \u201csource\u201d Markdown, such as in Jupyter Notebooks.</p><p>If the first element within the <code class=\"docutils literal notranslate\"><span class=\"pre\">div</span></code> is <code class=\"docutils literal notranslate\"><span class=\"pre\">&lt;div</span> <span class=\"pre\">class=\"title\"&gt;</span></code> or <code class=\"docutils literal notranslate\"><span class=\"pre\">&lt;p</span> <span class=\"pre\">class=\"title\"&gt;</span></code>, then this will be set as the admonition title.\nAll internal text (and the title) will be parsed as MyST-Markdown and all classes and an optional name will be passed to the admonition:</p>", "a[href=\"#html-admonitions\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">HTML Admonitions<a class=\"headerlink\" href=\"#html-admonitions\" title=\"Link to this heading\">\uf0c1</a></h2><p>By adding <code class=\"docutils literal notranslate\"><span class=\"pre\">\"html_admonition\"</span></code> to <code class=\"docutils literal notranslate\"><span class=\"pre\">myst_enable_extensions</span></code> (in the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code>),\nyou can enable parsing of <code class=\"docutils literal notranslate\"><span class=\"pre\">&lt;div</span> <span class=\"pre\">class=\"admonition\"&gt;</span></code> HTML blocks.\nThese blocks will be converted internally to Sphinx admonition directives, and so will work correctly for all output formats.\nThis is helpful when you care about viewing the \u201csource\u201d Markdown, such as in Jupyter Notebooks.</p><p>If the first element within the <code class=\"docutils literal notranslate\"><span class=\"pre\">div</span></code> is <code class=\"docutils literal notranslate\"><span class=\"pre\">&lt;div</span> <span class=\"pre\">class=\"title\"&gt;</span></code> or <code class=\"docutils literal notranslate\"><span class=\"pre\">&lt;p</span> <span class=\"pre\">class=\"title\"&gt;</span></code>, then this will be set as the admonition title.\nAll internal text (and the title) will be parsed as MyST-Markdown and all classes and an optional name will be passed to the admonition:</p>", "a[href=\"#syntax-extensions\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Syntax Extensions<a class=\"headerlink\" href=\"#syntax-extensions\" title=\"Link to this heading\">\uf0c1</a></h1><p>The following syntaxes are optional (disabled by default) and can be enabled\n<em>via</em> the sphinx <code class=\"docutils literal notranslate\"><span class=\"pre\">conf.py</span></code> (see also\n<a class=\"reference external\" href=\"https://myst-parser.readthedocs.io/en/latest/configuration.html#sphinx-config-options\">Configuration</a>).\nTheir goal is generally to add more <em>Markdown friendly</em> syntaxes; often enabling\nand rendering markdown-it-py plugins that extend the\n<a class=\"reference external\" href=\"https://commonmark.org/\">CommonMark specification</a>.</p><p>To enable all the syntaxes explained below:</p>"}
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
