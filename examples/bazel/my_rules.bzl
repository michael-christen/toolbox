# XXX: What can ctx be?
def _foo_binary_impl(ctx):
    # XXX: How to get toolchain specifics into the rule
    out = ctx.actions.declare_file(ctx.label.name)
    ctx.actions.write(
        output = out,
        # XXX: Different toolchain should have different prefix :shrug:
        content = "Hello {}!\n".format(ctx.attr.username),
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
)
