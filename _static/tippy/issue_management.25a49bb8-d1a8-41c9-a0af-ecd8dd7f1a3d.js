selector_to_html = {"a[href=\"#issue-management\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">Issue Management<a class=\"headerlink\" href=\"#issue-management\" title=\"Link to this heading\">\uf0c1</a></h1><p>This document describes how issues and pull requests are organized in this\nrepository.</p>", "a[href=\"#milestones\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Milestones<a class=\"headerlink\" href=\"#milestones\" title=\"Link to this heading\">\uf0c1</a></h2><p>Milestones group related issues by theme. An issue should be assigned to the\nmost relevant milestone; it is fine to leave an issue without a milestone if it\ndoes not fit any theme.</p>", "a[href=\"#project-board\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Project Board<a class=\"headerlink\" href=\"#project-board\" title=\"Link to this heading\">\uf0c1</a></h2><p>All open issues and PRs are tracked in the\n<a class=\"reference external\" href=\"https://github.com/users/michael-christen/projects/4\">Toolbox: All</a> GitHub\nproject. New issues and PRs should be added to this project when created.\nGitHub\u2019s project \u201cAuto-add\u201d workflow (under project Settings \u2192 Workflows) can\nautomate this.</p>", "a[href=\"#priorities\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Priorities<a class=\"headerlink\" href=\"#priorities\" title=\"Link to this heading\">\uf0c1</a></h2><p>Priorities are set on the project board using the <strong>Priority</strong> field.</p>", "a[href=\"#labels\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Labels<a class=\"headerlink\" href=\"#labels\" title=\"Link to this heading\">\uf0c1</a></h2><p>Labels describe the nature of the work.</p>", "a[href=\"#workflow\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\">Workflow<a class=\"headerlink\" href=\"#workflow\" title=\"Link to this heading\">\uf0c1</a></h2>"}
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
