load("@aspect_rules_js//js:defs.bzl", "js_library")
load("@npm//:defs.bzl", "npm_link_all_packages")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")

package(default_visibility = ["//visibility:public"])

compile_pip_requirements(
    name = "requirements",
)

npm_link_all_packages(name = "node_modules")

exports_files(
    [
        "buf.yaml",
        ".flake8",
        "pmd.xml",
        ".ruff.toml",
        ".shellcheckrc",
        ".scalafmt.conf",
    ],
    visibility = ["//visibility:public"],
)

js_library(
    name = "eslintrc",
    srcs = [".eslintrc.cjs"],
    deps = [
        ":node_modules/@typescript-eslint/eslint-plugin",
        ":node_modules/@typescript-eslint/parser",
    ],
)

# NB: this alias does NOT cause Bazel's Loading phase to load the tools/BUILD file.
# That's important as we don't want users to wait for "Eager fetching" for ~EVERY language which
# that build file loads from.
# Demonstration: we'll build the js_library above, then build this format alias, and see that many
# more repositories were fetched for the latter:
#  % export T=$(mktemp -d)
#  % bazel --output_base=$T build :eslintrc; ls $T/external > one
#  % bazel --output_base=$T build :format; ls $T/external > two
#  % wc -l one two
#    738 one
#    936 two
alias(
    name = "format",
    actual = "//tools:format",
)
