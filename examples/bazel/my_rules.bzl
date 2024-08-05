FooInfo = provider(
    doc = "Information to foo_binary, to add to output.",
    # XXX: More type-hinting or docs?
    fields = ["prefix"],
)

# XXX: What can ctx be?
def _foo_binary_impl(ctx):
    # XXX: How to get toolchain specifics into the rule
    out = ctx.actions.declare_file(ctx.label.name)
    info = ctx.toolchains[":toolchain_type"].fooinfo
    ctx.actions.write(
        output = out,
        # XXX: Different toolchain should have different prefix :shrug:
        content = "Hello from {} to {}!\n".format(
            info.prefix,
            ctx.attr.username,
        ),
    )

    # XXX: What is in global namespace
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
    # XXX: Making executable so we can do platform transitions
    # executable = True,
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

# XXX: Add constraint values
