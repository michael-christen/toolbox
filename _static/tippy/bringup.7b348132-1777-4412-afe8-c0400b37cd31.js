selector_to_html = {"a[href=\"#log-for-how-i-am-bringing-up-this-repo-and-my-new-server\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Log for How I am Bringing up This Repo and My New Server<a class=\"headerlink\" href=\"#log-for-how-i-am-bringing-up-this-repo-and-my-new-server\" title=\"Link to this heading\">\uf0c1</a></h1><h2>Log<a class=\"headerlink\" href=\"#log\" title=\"Link to this heading\">\uf0c1</a></h2><p>2023-12-27, Wednesday:</p>", "a[href=\"#log\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Log<a class=\"headerlink\" href=\"#log\" title=\"Link to this heading\">\uf0c1</a></h2><p>2023-12-27, Wednesday:</p>"}
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
