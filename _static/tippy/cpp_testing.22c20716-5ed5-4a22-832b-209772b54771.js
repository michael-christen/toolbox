selector_to_html = {"a[href=\"#c-testing\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">C++ Testing<a class=\"headerlink\" href=\"#c-testing\" title=\"Link to this heading\">\uf0c1</a></h1><p><code class=\"docutils literal notranslate\"><span class=\"pre\">cc_test</span></code> (from <code class=\"docutils literal notranslate\"><span class=\"pre\">//bzl:cc.bzl</span></code>) is the single rule for all C++ tests. It\nauto-selects the right underlying framework based on your includes:</p>", "a[href=\"#pw-log-in-pigweed-tests\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\"><code class=\"docutils literal notranslate\"><span class=\"pre\">PW_LOG_*</span></code> in Pigweed tests<a class=\"headerlink\" href=\"#pw-log-in-pigweed-tests\" title=\"Link to this heading\">\uf0c1</a></h2><p><code class=\"docutils literal notranslate\"><span class=\"pre\">PW_LOG_INFO</span></code>, <code class=\"docutils literal notranslate\"><span class=\"pre\">PW_LOG_DEBUG</span></code>, etc. are visible in test output. The log backend\nchain is:</p>", "a[href=\"#pigweed-integrated-tests\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Pigweed-integrated tests<a class=\"headerlink\" href=\"#pigweed-integrated-tests\" title=\"Link to this heading\">\uf0c1</a></h2><p>Include <code class=\"docutils literal notranslate\"><span class=\"pre\">pw_unit_test/framework.h</span></code> to opt in to Pigweed integration (gazelle\nadds <code class=\"docutils literal notranslate\"><span class=\"pre\">@pigweed//pw_unit_test</span></code> to deps automatically):</p>", "a[href=\"#host-only-tests\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Host-only tests<a class=\"headerlink\" href=\"#host-only-tests\" title=\"Link to this heading\">\uf0c1</a></h2><p><strong>References:</strong></p>"}
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
