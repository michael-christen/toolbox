selector_to_html = {"a[href=\"#module-contents\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Module Contents<a class=\"headerlink\" href=\"#module-contents\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#module-examples.basic.hello_test\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">examples.basic.hello_test<a class=\"headerlink\" href=\"#module-examples.basic.hello_test\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Classes<a class=\"headerlink\" href=\"#classes\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#classes\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Classes<a class=\"headerlink\" href=\"#classes\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#examples.basic.hello_test.TestHello.test_basics\"]": "<dt class=\"sig sig-object py\" id=\"examples.basic.hello_test.TestHello.test_basics\">\n<span class=\"sig-name descname\"><span class=\"pre\">test_basics</span></span><span class=\"sig-paren\">(</span><span class=\"sig-paren\">)</span><a class=\"reference internal\" href=\"../../../../_modules/examples/basic/hello_test.html#TestHello.test_basics\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd></dd>", "a[href=\"#examples.basic.hello_test.TestHello\"]": "<dt class=\"sig sig-object py\" id=\"examples.basic.hello_test.TestHello\">\n<em class=\"property\"><span class=\"pre\">class</span><span class=\"w\"> </span></em><span class=\"sig-prename descclassname\"><span class=\"pre\">examples.basic.hello_test.</span></span><span class=\"sig-name descname\"><span class=\"pre\">TestHello</span></span><span class=\"sig-paren\">(</span><em class=\"sig-param\"><span class=\"n\"><span class=\"pre\">methodName</span></span><span class=\"o\"><span class=\"pre\">=</span></span><span class=\"default_value\"><span class=\"pre\">'runTest'</span></span></em><span class=\"sig-paren\">)</span><a class=\"reference internal\" href=\"../../../../_modules/examples/basic/hello_test.html#TestHello\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd><p>Bases: <code class=\"xref py py-obj docutils literal notranslate\"><span class=\"pre\">unittest.TestCase</span></code></p><p>Test proto loading.</p></dd>"}
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
