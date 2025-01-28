selector_to_html = {"a[href=\"#module-contents\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Module Contents<a class=\"headerlink\" href=\"#module-contents\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#examples.basic.server.Greeter\"]": "<dt class=\"sig sig-object py\" id=\"examples.basic.server.Greeter\">\n<em class=\"property\"><span class=\"pre\">class</span><span class=\"w\"> </span></em><span class=\"sig-prename descclassname\"><span class=\"pre\">examples.basic.server.</span></span><span class=\"sig-name descname\"><span class=\"pre\">Greeter</span></span><a class=\"reference internal\" href=\"../../../../_modules/examples/basic/server.html#Greeter\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd><p>Bases: <a class=\"reference internal\" href=\"../hello_pb2_grpc/index.html#examples.basic.hello_pb2_grpc.GreeterServicer\" title=\"examples.basic.hello_pb2_grpc.GreeterServicer\"><code class=\"xref py py-obj docutils literal notranslate\"><span class=\"pre\">examples.basic.hello_pb2_grpc.GreeterServicer</span></code></a></p></dd>", "a[href=\"#examples.basic.server.get_server\"]": "<dt class=\"sig sig-object py\" id=\"examples.basic.server.get_server\">\n<span class=\"sig-prename descclassname\"><span class=\"pre\">examples.basic.server.</span></span><span class=\"sig-name descname\"><span class=\"pre\">get_server</span></span><span class=\"sig-paren\">(</span><span class=\"sig-paren\">)</span> <span class=\"sig-return\"><span class=\"sig-return-icon\">\u2192</span> <span class=\"sig-return-typehint\"><span class=\"pre\">grpc.aio.Server</span></span></span><a class=\"reference internal\" href=\"../../../../_modules/examples/basic/server.html#get_server\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd></dd>", "a[href=\"#examples.basic.server.Greeter.SayHello\"]": "<dt class=\"sig sig-object py\" id=\"examples.basic.server.Greeter.SayHello\">\n<em class=\"property\"><span class=\"pre\">async</span><span class=\"w\"> </span></em><span class=\"sig-name descname\"><span class=\"pre\">SayHello</span></span><span class=\"sig-paren\">(</span><em class=\"sig-param\"><span class=\"n\"><span class=\"pre\">request</span></span><span class=\"p\"><span class=\"pre\">:</span></span><span class=\"w\"> </span><span class=\"n\"><span class=\"pre\">examples.basic.hello_pb2.HelloRequest</span></span></em>, <em class=\"sig-param\"><span class=\"n\"><span class=\"pre\">context</span></span><span class=\"p\"><span class=\"pre\">:</span></span><span class=\"w\"> </span><span class=\"n\"><span class=\"pre\">grpc.aio.ServicerContext</span></span></em><span class=\"sig-paren\">)</span> <span class=\"sig-return\"><span class=\"sig-return-icon\">\u2192</span> <span class=\"sig-return-typehint\"><span class=\"pre\">examples.basic.hello_pb2.HelloReply</span></span></span><a class=\"reference internal\" href=\"../../../../_modules/examples/basic/server.html#Greeter.SayHello\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd></dd>", "a[href=\"#classes\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Classes<a class=\"headerlink\" href=\"#classes\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#functions\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#module-examples.basic.server\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">examples.basic.server<a class=\"headerlink\" href=\"#module-examples.basic.server\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Classes<a class=\"headerlink\" href=\"#classes\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"../hello_pb2_grpc/index.html#examples.basic.hello_pb2_grpc.GreeterServicer\"]": "<dt class=\"sig sig-object py\" id=\"examples.basic.hello_pb2_grpc.GreeterServicer\">\n<em class=\"property\"><span class=\"pre\">class</span><span class=\"w\"> </span></em><span class=\"sig-prename descclassname\"><span class=\"pre\">examples.basic.hello_pb2_grpc.</span></span><span class=\"sig-name descname\"><span class=\"pre\">GreeterServicer</span></span><a class=\"reference internal\" href=\"../../../../_modules/examples/basic/hello_pb2_grpc.html#GreeterServicer\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd><p>Bases: <code class=\"xref py py-obj docutils literal notranslate\"><span class=\"pre\">object</span></code></p><p>Missing associated documentation comment in .proto file.</p></dd>", "a[href=\"#examples.basic.server.serve\"]": "<dt class=\"sig sig-object py\" id=\"examples.basic.server.serve\">\n<em class=\"property\"><span class=\"k\"><span class=\"pre\">async</span></span><span class=\"w\"> </span></em><span class=\"sig-prename descclassname\"><span class=\"pre\">examples.basic.server.</span></span><span class=\"sig-name descname\"><span class=\"pre\">serve</span></span><span class=\"sig-paren\">(</span><span class=\"sig-paren\">)</span> <span class=\"sig-return\"><span class=\"sig-return-icon\">\u2192</span> <span class=\"sig-return-typehint\"><span class=\"pre\">None</span></span></span><a class=\"reference internal\" href=\"../../../../_modules/examples/basic/server.html#serve\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd></dd>"}
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
