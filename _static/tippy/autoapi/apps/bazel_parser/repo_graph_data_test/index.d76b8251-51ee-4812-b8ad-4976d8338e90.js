selector_to_html = {"a[href=\"#apps.bazel_parser.repo_graph_data_test.TestRepoGraphData\"]": "<dt class=\"sig sig-object py\" id=\"apps.bazel_parser.repo_graph_data_test.TestRepoGraphData\">\n<em class=\"property\"><span class=\"k\"><span class=\"pre\">class</span></span><span class=\"w\"> </span></em><span class=\"sig-prename descclassname\"><span class=\"pre\">apps.bazel_parser.repo_graph_data_test.</span></span><span class=\"sig-name descname\"><span class=\"pre\">TestRepoGraphData</span></span><span class=\"sig-paren\">(</span><em class=\"sig-param\"><span class=\"n\"><span class=\"pre\">methodName</span></span><span class=\"o\"><span class=\"pre\">=</span></span><span class=\"default_value\"><span class=\"pre\">'runTest'</span></span></em><span class=\"sig-paren\">)</span><a class=\"reference internal\" href=\"../../../../_modules/apps/bazel_parser/repo_graph_data_test.html#TestRepoGraphData\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd><p>Bases: <code class=\"xref py py-obj docutils literal notranslate\"><span class=\"pre\">unittest.TestCase</span></code></p><p>A class whose instances are single test cases.</p><p>By default, the test code itself should be placed in a method named\n\u2018runTest\u2019.</p><p>If the fixture may be used for many test cases, create as\nmany test methods as are needed. When instantiating such a TestCase\nsubclass, specify in the constructor arguments the name of the test method\nthat the instance is to execute.</p><p>Test authors should subclass TestCase for their own tests. Construction\nand deconstruction of the test\u2019s environment (\u2018fixture\u2019) can be\nimplemented by overriding the \u2018setUp\u2019 and \u2018tearDown\u2019 methods respectively.</p><p>If it is necessary to override the __init__ method, the base class\n__init__ method must always be called. It is important that subclasses\nshould not change the signature of their __init__ method, since instances\nof the classes are instantiated automatically by parts of the framework\nin order to be run.</p></dd>", "a[href=\"#module-apps.bazel_parser.repo_graph_data_test\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">apps.bazel_parser.repo_graph_data_test<a class=\"headerlink\" href=\"#module-apps.bazel_parser.repo_graph_data_test\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Classes<a class=\"headerlink\" href=\"#classes\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#classes\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Classes<a class=\"headerlink\" href=\"#classes\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#apps.bazel_parser.repo_graph_data_test.TestRepoGraphData.test_basics\"]": "<dt class=\"sig sig-object py\" id=\"apps.bazel_parser.repo_graph_data_test.TestRepoGraphData.test_basics\">\n<span class=\"sig-name descname\"><span class=\"pre\">test_basics</span></span><span class=\"sig-paren\">(</span><span class=\"sig-paren\">)</span> <span class=\"sig-return\"><span class=\"sig-return-icon\">\u2192</span> <span class=\"sig-return-typehint\"><span class=\"pre\">None</span></span></span><a class=\"reference internal\" href=\"../../../../_modules/apps/bazel_parser/repo_graph_data_test.html#TestRepoGraphData.test_basics\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd></dd>", "a[href=\"#module-contents\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Module Contents<a class=\"headerlink\" href=\"#module-contents\" title=\"Link to this heading\">\uf0c1</a></h2>"}
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
