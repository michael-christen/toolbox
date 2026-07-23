load("@rules_python//python:defs.bzl", "py_binary")

# Regenerate with: bazel run //examples/register_description:gen_header
# (requires peakrdl in requirements_lock.txt; see README for status)
genrule(
    name = "gen_header",
    srcs = ["lsm6dso_subset.rdl"],
    outs = ["lsm6dso_subset.h"],
    # peakrdl is not yet in requirements.in; this documents the intended
    # invocation. Run manually: peakrdl c-header --bitfields ltoh -o ... ...
    cmd = "peakrdl c-header --bitfields ltoh -o $@ $(location lsm6dso_subset.rdl)",
    tags = ["manual"],
)

genrule(
    name = "gen_html",
    srcs = ["lsm6dso_subset.rdl"],
    outs = ["html_docs.zip"],
    cmd = """
        tmp=$$(mktemp -d)
        peakrdl html $(location lsm6dso_subset.rdl) -o $$tmp
        zip -r $@ $$tmp
    """,
    tags = ["manual"],
)
