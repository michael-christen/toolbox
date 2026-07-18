"""Enable copt transitions for executables."""

def _copts_transition_impl(settings, attr):
    # Replace global copt flags with the ones in this rule
    return {
        "//command_line_option:copt": attr.extra_copts,
    }

copts_transition = transition(
    implementation = _copts_transition_impl,
    inputs = [],
    outputs = ["//command_line_option:copt"],
)

def _wrapper_impl(ctx):
    wrapped = ctx.attr.wrapped[DefaultInfo]

    # Copy delegate's executable into our own output, otherwise bazel complains
    # about the executable.
    out = ctx.actions.declare_file(ctx.label.name)
    ctx.actions.run_shell(
        inputs = [wrapped.files_to_run.executable],
        outputs = [out],
        command = "cp $1 $2",
        arguments = [
            wrapped.files_to_run.executable.path,
            out.path,
        ],
    )
    return DefaultInfo(executable = out)

executable_with_copts = rule(
    implementation = _wrapper_impl,
    attrs = {
        "wrapped": attr.label(),
        "extra_copts": attr.string_list(),
    },
    cfg = copts_transition,
)
