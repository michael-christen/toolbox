selector_to_html = {"a[href=\"examples/basic/hello_pb2_grpc/index.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">examples.basic.hello_pb2_grpc<a class=\"headerlink\" href=\"#module-examples.basic.hello_pb2_grpc\" title=\"Link to this heading\">\uf0c1</a></h1><p>Client and server classes corresponding to protobuf-defined services.</p>", "a[href=\"examples/basic/hello_test/index.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">examples.basic.hello_test<a class=\"headerlink\" href=\"#module-examples.basic.hello_test\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Classes<a class=\"headerlink\" href=\"#classes\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"examples/basic/main/index.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">examples.basic.main<a class=\"headerlink\" href=\"#module-examples.basic.main\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#api-reference\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">API Reference<a class=\"headerlink\" href=\"#api-reference\" title=\"Link to this heading\">\uf0c1</a></h1><p>This page contains auto-generated API reference documentation <a class=\"footnote-reference brackets\" href=\"#f1\" id=\"id1\" role=\"doc-noteref\"><span class=\"fn-bracket\">[</span>1<span class=\"fn-bracket\">]</span></a>.</p>", "a[href=\"examples/basic/client/index.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">examples.basic.client<a class=\"headerlink\" href=\"#module-examples.basic.client\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"examples/basic/hello_pb2/index.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">examples.basic.hello_pb2<a class=\"headerlink\" href=\"#module-examples.basic.hello_pb2\" title=\"Link to this heading\">\uf0c1</a></h1><p>Generated protocol buffer code.</p>", "a[href=\"#f1\"]": "<aside class=\"footnote brackets\" id=\"f1\" role=\"doc-footnote\">\n<span class=\"label\"><span class=\"fn-bracket\">[</span><a href=\"#id1\" role=\"doc-backlink\">1</a><span class=\"fn-bracket\">]</span></span>\n<p>Created with <a class=\"reference external\" href=\"https://github.com/readthedocs/sphinx-autoapi\">sphinx-autoapi</a></p>\n</aside>", "a[href=\"examples/basic/server/index.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">examples.basic.server<a class=\"headerlink\" href=\"#module-examples.basic.server\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Classes<a class=\"headerlink\" href=\"#classes\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"examples/basic/grpc_test/index.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">examples.basic.grpc_test<a class=\"headerlink\" href=\"#module-examples.basic.grpc_test\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Classes<a class=\"headerlink\" href=\"#classes\" title=\"Link to this heading\">\uf0c1</a></h2>"}
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
