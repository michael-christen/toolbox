selector_to_html = {"a[href=\"#c-testing\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">C++ Testing<a class=\"headerlink\" href=\"#c-testing\" title=\"Link to this heading\">\uf0c1</a></h1><p>Two build rules are used for C++ tests, depending on whether Pigweed integration\nis required.</p>", "a[href=\"#cc-test-host-unit-tests\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\"><code class=\"docutils literal notranslate\"><span class=\"pre\">cc_test</span></code> \u2014 host unit tests<a class=\"headerlink\" href=\"#cc-test-host-unit-tests\" title=\"Link to this heading\">\uf0c1</a></h2><p>Use <code class=\"docutils literal notranslate\"><span class=\"pre\">cc_test</span></code> (from <code class=\"docutils literal notranslate\"><span class=\"pre\">//bzl:cc.bzl</span></code>) for tests that run purely on the host with\nno Pigweed backends. Gazelle auto-generates the BUILD target and wires in\n<code class=\"docutils literal notranslate\"><span class=\"pre\">//tlbox/testing:gtest_main</span></code>.</p>", "a[href=\"#why-two-rules\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Why two rules?<a class=\"headerlink\" href=\"#why-two-rules\" title=\"Link to this heading\">\uf0c1</a></h2><p><code class=\"docutils literal notranslate\"><span class=\"pre\">pw_cc_test</span></code> pulls in Pigweed\u2019s build system integration: facade backends,\nlinker scripts, and the <code class=\"docutils literal notranslate\"><span class=\"pre\">pw_unit_test</span></code> framework. <code class=\"docutils literal notranslate\"><span class=\"pre\">cc_test</span></code> doesn\u2019t need any of\nthat for pure host tests. The test <em>syntax</em> is identical (both use the Google\nTest API); only the build rule differs.</p>", "a[href=\"#pw-log-in-pw-cc-test\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\"><code class=\"docutils literal notranslate\"><span class=\"pre\">PW_LOG_*</span></code> in <code class=\"docutils literal notranslate\"><span class=\"pre\">pw_cc_test</span></code><a class=\"headerlink\" href=\"#pw-log-in-pw-cc-test\" title=\"Link to this heading\">\uf0c1</a></h2><p><code class=\"docutils literal notranslate\"><span class=\"pre\">PW_LOG_INFO</span></code>, <code class=\"docutils literal notranslate\"><span class=\"pre\">PW_LOG_DEBUG</span></code>, etc. are visible in <code class=\"docutils literal notranslate\"><span class=\"pre\">pw_cc_test</span></code> output. The log\nbackend chain is:</p>", "a[href=\"#pw-cc-test-pigweed-integrated-tests\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\"><code class=\"docutils literal notranslate\"><span class=\"pre\">pw_cc_test</span></code> \u2014 Pigweed-integrated tests<a class=\"headerlink\" href=\"#pw-cc-test-pigweed-integrated-tests\" title=\"Link to this heading\">\uf0c1</a></h2><p>Use <code class=\"docutils literal notranslate\"><span class=\"pre\">pw_cc_test</span></code> (from <code class=\"docutils literal notranslate\"><span class=\"pre\">//bzl:cc.bzl</span></code>) for tests that need Pigweed backends \u2014\nI2C mocks, async dispatchers, allocator testing, etc. These use the same Google\nTest API (<code class=\"docutils literal notranslate\"><span class=\"pre\">TEST</span></code>, <code class=\"docutils literal notranslate\"><span class=\"pre\">EXPECT_*</span></code>, <code class=\"docutils literal notranslate\"><span class=\"pre\">ASSERT_*</span></code>) as <code class=\"docutils literal notranslate\"><span class=\"pre\">cc_test</span></code>.</p>"}
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
