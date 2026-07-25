selector_to_html = {"a[href=\"#myst\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">MyST<a class=\"headerlink\" href=\"#myst\" title=\"Link to this heading\">\uf0c1</a></h1><p>Great news, we don\u2019t have to use .rst, we can leverage\n<a class=\"reference external\" href=\"https://mystmd.org/\">MyST</a> to write markdown.</p><p>MyST makes Markdown more <em>extensible</em> &amp; <strong>powerful</strong> to support an ecosystem of\ntools for computational narratives, technical documentation, and open scientific\ncommunication.</p>"}
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
