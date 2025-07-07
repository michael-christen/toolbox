selector_to_html = {"a[href=\"#module-examples.basic.client\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">examples.basic.client<a class=\"headerlink\" href=\"#module-examples.basic.client\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#module-contents\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Module Contents<a class=\"headerlink\" href=\"#module-contents\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#examples.basic.client.get_response\"]": "<dt class=\"sig sig-object py\" id=\"examples.basic.client.get_response\">\n<em class=\"property\"><span class=\"k\"><span class=\"pre\">async</span></span><span class=\"w\"> </span></em><span class=\"sig-prename descclassname\"><span class=\"pre\">examples.basic.client.</span></span><span class=\"sig-name descname\"><span class=\"pre\">get_response</span></span><span class=\"sig-paren\">(</span><span class=\"sig-paren\">)</span> <span class=\"sig-return\"><span class=\"sig-return-icon\">\u2192</span> <span class=\"sig-return-typehint\"><span class=\"pre\">examples.basic.hello_pb2.HelloReply</span></span></span><a class=\"reference internal\" href=\"../../../../_modules/examples/basic/client.html#get_response\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd><p>Establish a connection, send hello and return the reply.</p><p>Asyncyhronous.</p></dd>", "a[href=\"#functions\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#examples.basic.client.run\"]": "<dt class=\"sig sig-object py\" id=\"examples.basic.client.run\">\n<em class=\"property\"><span class=\"k\"><span class=\"pre\">async</span></span><span class=\"w\"> </span></em><span class=\"sig-prename descclassname\"><span class=\"pre\">examples.basic.client.</span></span><span class=\"sig-name descname\"><span class=\"pre\">run</span></span><span class=\"sig-paren\">(</span><span class=\"sig-paren\">)</span> <span class=\"sig-return\"><span class=\"sig-return-icon\">\u2192</span> <span class=\"sig-return-typehint\"><span class=\"pre\">None</span></span></span><a class=\"reference internal\" href=\"../../../../_modules/examples/basic/client.html#run\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd></dd>"}
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
