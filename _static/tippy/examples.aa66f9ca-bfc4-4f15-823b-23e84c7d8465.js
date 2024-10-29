selector_to_html = {"a[href=\"#section-two\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Here\u2019s another section<a class=\"headerlink\" href=\"#heres-another-section\" title=\"Link to this heading\">\uf0c1</a></h2><p>And some more content.</p><p><a class=\"reference internal\" href=\"#section-two\"><span class=\"std std-ref\">a reference to this section</span></a>. I can also reference the\nsection <a class=\"reference internal\" href=\"#section-two\"><span class=\"std std-ref\">Here\u2019s another section</span></a> without specifying my title.</p>", "a[href=\"#heres-another-section\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Here\u2019s another section<a class=\"headerlink\" href=\"#heres-another-section\" title=\"Link to this heading\">\uf0c1</a></h2><p>And some more content.</p><p><a class=\"reference internal\" href=\"#section-two\"><span class=\"std std-ref\">a reference to this section</span></a>. I can also reference the\nsection <a class=\"reference internal\" href=\"#section-two\"><span class=\"std std-ref\">Here\u2019s another section</span></a> without specifying my title.</p>", "a[href=\"#my-nifty-title\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">My nifty title<a class=\"headerlink\" href=\"#my-nifty-title\" title=\"Link to this heading\">\uf0c1</a></h1><p>Some <strong>text</strong>!</p>"}
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
