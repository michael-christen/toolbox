selector_to_html = {"a[href=\"#argument-shortcuts\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Argument shortcuts<a class=\"headerlink\" href=\"#argument-shortcuts\" title=\"Link to this heading\">\uf0c1</a></h3><p><a class=\"reference external\" href=\"https://stackoverflow.com/questions/4009412/how-to-use-arguments-from-previous-command\">https://stackoverflow.com/questions/4009412/how-to-use-arguments-from-previous-command</a></p>", "a[href=\"#reload-udev-rules\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Reload udev rules:<a class=\"headerlink\" href=\"#reload-udev-rules\" title=\"Link to this heading\">\uf0c1</a></h2>", "a[href=\"#bash\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Bash<a class=\"headerlink\" href=\"#bash\" title=\"Link to this heading\">\uf0c1</a></h2><h3>Argument shortcuts<a class=\"headerlink\" href=\"#argument-shortcuts\" title=\"Link to this heading\">\uf0c1</a></h3><p><a class=\"reference external\" href=\"https://stackoverflow.com/questions/4009412/how-to-use-arguments-from-previous-command\">https://stackoverflow.com/questions/4009412/how-to-use-arguments-from-previous-command</a></p>", "a[href=\"#package-commands\"]": "<h3 class=\"tippy-header\" style=\"margin-top: 0;\">Package Commands<a class=\"headerlink\" href=\"#package-commands\" title=\"Link to this heading\">\uf0c1</a></h3><p>Get package dependencies:</p>", "a[href=\"#useful-commands\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Useful Commands<a class=\"headerlink\" href=\"#useful-commands\" title=\"Link to this heading\">\uf0c1</a></h1><p>This is just a place for me to put small commands that I find myself looking up\nfrequently.</p>"}
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
