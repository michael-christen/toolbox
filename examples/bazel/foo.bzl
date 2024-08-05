def _foo_binary_impl(ctx):
    print("analyzing", ctx.label)
    out = ctx.actions.declare_file(ctx.label.name)
    ctx.actions.write(
        output = out,
        content = "Hello {}!\n".format(ctx.attr.username),
    )
    # In order to communicate outputs of the rule
    return [DefaultInfo(files = depset([out]))]

foo_binary = rule(
    # Define callback
    implementation = _foo_binary_impl,
    # Define arguments
    attrs = {
        "username": attr.string(),
    },
)

print("bzl file evaluation")

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

"""
_core_headers = [...]  # private constant representing standard library files

# Keyword-only arguments are preferred.
def _exampleinfo_init(*, files_to_link, headers = None, allow_empty_files_to_link = False):
    if not files_to_link and not allow_empty_files_to_link:
        fail("files_to_link may not be empty")
    all_headers = depset(_core_headers, transitive = headers)
    return {"files_to_link": files_to_link, "headers": all_headers}

ExampleInfo, _new_exampleinfo = provider(
    "Info needed to compile/link Example code.",
    fields = {
        "headers": "depset of header Files from transitive dependencies.",
        "files_to_link": "depset of Files from compilation.",
    },
    init = _exampleinfo_init,
)

def make_barebones_exampleinfo(headers):
    # Returns an ExampleInfo with no files_to_link and only the specified headers.
    return _new_exampleinfo(files_to_link = depset(), headers = all_headers)

def _example_library_impl(ctx):
    ...

    transitive_headers = [dep[ExampleInfo].headers for dep in ctx.attr.deps]
    headers = depset(ctx.files.hdrs, transitive = transitive_headers)
    srcs = ctx.files.srcs
    inputs = depset(srcs, transitive = [headers])
    output_file = ctx.actions.declare_file(ctx.label.name + ".output")

    args = ctx.actions.args()
    args.add_joined("-h", headers, join_with = ",")
    args.add_joined("-s", srcs, join_with = ",")
    args.add("-o", output_file)

    ctx.actions.run(
        mnemonic = "ExampleCompile",
        executable = ctx.executable._compiler,
        arguments = [args],
        inputs = inputs,
        outputs = [output_file],
    )
    ...
    runfiles = ctx.runfiles(files = ctx.files.data)
    transitive_runfiles = []
    for runfiles_attr in (
        ctx.attr.srcs,
        ctx.attr.hdrs,
        ctx.attr.deps,
        ctx.attr.data,
    ):
        for target in runfiles_attr:
            transitive_runfiles.append(target[DefaultInfo].default_runfiles)
    runfiles = runfiles.merge_all(transitive_runfiles)
    return [
        DefaultInfo(..., runfiles = runfiles),
        ExampleInfo(
          headers = headers,
          files_to_link = depset(
              [output_file],
              transitive = [
                  dep[ExampleInfo].files_to_link for dep in ctx.attr.deps
              ],
          ),
        ),
    ]


def _rule_with_validation_impl(ctx):

  ctx.actions.write(ctx.outputs.main, "main output\n")
  ctx.actions.write(ctx.outputs.implicit, "implicit output\n")

  validation_output = ctx.actions.declare_file(ctx.attr.name + ".validation")
  ctx.actions.run(
    outputs = [validation_output],
    executable = ctx.executable._validation_tool,
    arguments = [validation_output.path],
  )

  return [
    DefaultInfo(files = depset([ctx.outputs.main])),
    OutputGroupInfo(_validation = depset([validation_output])),
  ]


rule_with_validation = rule(
  implementation = _rule_with_validation_impl,
  outputs = {
    "main": "%{name}.main",
    "implicit": "%{name}.implicit",
  },
  attrs = {
    "_validation_tool": attr.label(
        default = Label("//validation_actions:validation_tool"),
        executable = True,
        cfg = "exec"
    ),
  }
)
"""

# depset

s = depset(["a", "b", "c"])
t = depset(["d", "e"], transitive = [s])

print(s)    # depset(["a", "b", "c"])
print(t)    # depset(["d", "e", "a", "b", "c"])

# aspect
def _print_aspect_impl(target, ctx):
    # Make sure the rule has a srcs attribute.
    if hasattr(ctx.rule.attr, 'srcs'):
        # Iterate through the files that make up the sources and
        # print their paths.
        for src in ctx.rule.attr.srcs:
            for f in src.files.to_list():
                print(f.path)
    return []

# Invoke as
# bazel build //... --aspects examples/bazel/foo.bzl%print_aspect

print_aspect = aspect(
    implementation = _print_aspect_impl,
    attr_aspects = ['deps'],
)
