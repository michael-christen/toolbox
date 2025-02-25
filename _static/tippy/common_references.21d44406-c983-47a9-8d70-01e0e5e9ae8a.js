selector_to_html = {"a[href=\"#common-references\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Common References<a class=\"headerlink\" href=\"#common-references\" title=\"Link to this heading\">\uf0c1</a></h1><p>Common references that are often used.</p>", "a[href=\"common/python_references.html#strings\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Strings<a class=\"headerlink\" href=\"#strings\" title=\"Link to this heading\">\uf0c1</a></h2><p><a class=\"reference external\" href=\"https://docs.python.org/3/library/string.html#format-specification-mini-language\">https://docs.python.org/3/library/string.html#format-specification-mini-language</a></p>", "a[href=\"common/python_references.html\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Python References<a class=\"headerlink\" href=\"#python-references\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Strings<a class=\"headerlink\" href=\"#strings\" title=\"Link to this heading\">\uf0c1</a></h2><p><a class=\"reference external\" href=\"https://docs.python.org/3/library/string.html#format-specification-mini-language\">https://docs.python.org/3/library/string.html#format-specification-mini-language</a></p>"}
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
