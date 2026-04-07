selector_to_html = {"a[href=\"#examples.basic.main.main\"]": "<dt class=\"sig sig-object py\" id=\"examples.basic.main.main\">\n<span class=\"sig-prename descclassname\"><span class=\"pre\">examples.basic.main.</span></span><span class=\"sig-name descname\"><span class=\"pre\">main</span></span><span class=\"sig-paren\">(</span><span class=\"sig-paren\">)</span><a class=\"reference internal\" href=\"../../../../_modules/examples/basic/main.html#main\"><span class=\"viewcode-link\"><span class=\"pre\">[source]</span></span></a></dt><dd></dd>", "a[href=\"#module-contents\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Module Contents<a class=\"headerlink\" href=\"#module-contents\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#module-examples.basic.main\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">examples.basic.main<a class=\"headerlink\" href=\"#module-examples.basic.main\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#functions\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Functions<a class=\"headerlink\" href=\"#functions\" title=\"Link to this heading\">\uf0c1</a></h2>"}
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
