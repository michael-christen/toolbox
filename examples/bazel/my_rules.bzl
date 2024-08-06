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
