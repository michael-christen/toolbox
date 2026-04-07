# https://bazel.build/extending/rules#providers
# https://bazel.build/rules/lib/globals/bzl#provider
FooInfo = provider(
    doc = "Information to foo_binary, to add to output.",
    # NOTE: Can also just define as a list
    fields = {
        "prefix": "Prefix used in assembling foo output",
    },
)

# ctx fields: https://bazel.build/rules/lib/builtins/ctx
def _foo_binary_impl(ctx):
    if not ctx.attr.username:
        fail("username must not be empty")

    # Get toolchain specifics into the rule
    info = ctx.toolchains[":toolchain_type"].fooinfo
    out = ctx.actions.declare_file(ctx.label.name)
    ctx.actions.write(
        output = out,
        # Different toolchain uses different prefix
        content = "Hello from {} to {}!\n".format(
            info.prefix,
            ctx.attr.username,
        ),
    )

    return [DefaultInfo(files = depset([out]))]

# A rule definition consists of an implementation and attrs (arguments)
# - A rule implementation is called with ctx and returns a list of providers
foo_binary = rule(
    implementation = _foo_binary_impl,
    attrs = {
        "username": attr.string(),
    },
    toolchains = [
        config_common.toolchain_type(":toolchain_type", mandatory = True),
    ],
)

def _foo_toolchain_impl(ctx):
    toolchain_info = platform_common.ToolchainInfo(
        fooinfo = FooInfo(
            prefix = ctx.attr.prefix,
        ),
    )
    return [toolchain_info]

foo_toolchain = rule(
    implementation = _foo_toolchain_impl,
    attrs = {
        "prefix": attr.string(),
    },
)

def _hello_world_impl(ctx):
    out = ctx.actions.declare_file(ctx.label.name + ".cc")
    ctx.actions.expand_template(
        output = out,
        template = ctx.file.template,
        substitutions = {"{NAME}": ctx.attr.username},
    )
    return [DefaultInfo(files = depset([out]))]

hello_world = rule(
    implementation = _hello_world_impl,
    attrs = {
        "username": attr.string(default = "unknown person"),
        "template": attr.label(
            allow_single_file = [".cc.tpl"],
            mandatory = True,
        ),
        # If we wanted private default
        # "_template": attr.label(
        #     allow_single_file = True,
        #     default = "file.cc.tpl",
        # ),
    },
)

# aspect
def _print_aspect_impl(target, ctx):
    # Make sure the rule has a srcs attribute.
    if hasattr(ctx.rule.attr, "srcs"):
        # Iterate through the files that make up the sources and
        # print their paths.
        for src in ctx.rule.attr.srcs:
            for f in src.files.to_list():
                print(f.path)
    return []

# Invoke as
# bazel build //... --aspects examples/bazel/my_rules.bzl%print_aspect

print_aspect = aspect(
    implementation = _print_aspect_impl,
    attr_aspects = ["deps"],
)
