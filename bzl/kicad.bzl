"""Bazel rules for KiCad EDA tooling via kicad-cli."""

def _kicad_schematic_svgs_impl(ctx):
    """Export all schematic sheets as SVGs into a directory tree artifact."""
    output_dir = ctx.actions.declare_directory(ctx.label.name)
    ctx.actions.run_shell(
        inputs = ctx.files.srcs,
        outputs = [output_dir],
        command = "kicad-cli sch export svg -o {out} {top}".format(
            out = output_dir.path,
            top = ctx.file.top.path,
        ),
        mnemonic = "KiCadSchematicSVG",
        progress_message = "Exporting schematic SVGs for {}".format(ctx.label.name),
    )
    return [DefaultInfo(files = depset([output_dir]))]

kicad_schematic_svgs = rule(
    implementation = _kicad_schematic_svgs_impl,
    doc = "Export a (possibly multi-sheet) schematic as SVG files into a directory.",
    attrs = {
        "top": attr.label(
            doc = "Top-level .kicad_sch file.",
            allow_single_file = [".kicad_sch"],
            mandatory = True,
        ),
        "srcs": attr.label_list(
            doc = "All .kicad_sch files (top-level + sub-sheets).",
            allow_files = [".kicad_sch"],
            mandatory = True,
        ),
    },
)

def _kicad_schematic_pdf_impl(ctx):
    """Export all schematic sheets as a single PDF."""
    output = ctx.actions.declare_file(ctx.label.name + ".pdf")
    ctx.actions.run_shell(
        inputs = ctx.files.srcs,
        outputs = [output],
        command = "kicad-cli sch export pdf -o {out} {top}".format(
            out = output.path,
            top = ctx.file.top.path,
        ),
        mnemonic = "KiCadSchematicPDF",
        progress_message = "Exporting schematic PDF for {}".format(ctx.label.name),
    )
    return [DefaultInfo(files = depset([output]))]

kicad_schematic_pdf = rule(
    implementation = _kicad_schematic_pdf_impl,
    doc = "Export a (possibly multi-sheet) schematic as a single PDF.",
    attrs = {
        "top": attr.label(
            doc = "Top-level .kicad_sch file.",
            allow_single_file = [".kicad_sch"],
            mandatory = True,
        ),
        "srcs": attr.label_list(
            doc = "All .kicad_sch files (top-level + sub-sheets).",
            allow_files = [".kicad_sch"],
            mandatory = True,
        ),
    },
)

def _kicad_pcb_svg_impl(ctx):
    """Export a PCB layout as SVG."""
    output = ctx.actions.declare_file(ctx.label.name + ".svg")
    ctx.actions.run_shell(
        inputs = [ctx.file.src],
        outputs = [output],
        command = "kicad-cli pcb export svg -o {out} {src}".format(
            out = output.path,
            src = ctx.file.src.path,
        ),
        mnemonic = "KiCadPCBSVG",
        progress_message = "Exporting PCB SVG for {}".format(ctx.label.name),
    )
    return [DefaultInfo(files = depset([output]))]

kicad_pcb_svg = rule(
    implementation = _kicad_pcb_svg_impl,
    doc = "Export a PCB layout as SVG.",
    attrs = {
        "src": attr.label(
            doc = "The .kicad_pcb file.",
            allow_single_file = [".kicad_pcb"],
            mandatory = True,
        ),
    },
)

def _kicad_gerbers_impl(ctx):
    """Export PCB gerber files into a directory tree artifact."""
    output_dir = ctx.actions.declare_directory(ctx.label.name)
    ctx.actions.run_shell(
        inputs = [ctx.file.src],
        outputs = [output_dir],
        command = "kicad-cli pcb export gerbers -o {out} {src}".format(
            out = output_dir.path,
            src = ctx.file.src.path,
        ),
        mnemonic = "KiCadGerbers",
        progress_message = "Exporting gerbers for {}".format(ctx.label.name),
    )
    return [DefaultInfo(files = depset([output_dir]))]

kicad_gerbers = rule(
    implementation = _kicad_gerbers_impl,
    doc = "Export PCB gerber files into a directory.",
    attrs = {
        "src": attr.label(
            doc = "The .kicad_pcb file.",
            allow_single_file = [".kicad_pcb"],
            mandatory = True,
        ),
    },
)

def _kicad_drc_impl(ctx):
    """Run DRC and produce a JSON report."""
    output = ctx.actions.declare_file(ctx.label.name + ".json")
    ctx.actions.run_shell(
        inputs = [ctx.file.src],
        outputs = [output],
        command = "kicad-cli pcb drc --format json -o {out} {src}".format(
            out = output.path,
            src = ctx.file.src.path,
        ),
        mnemonic = "KiCadDRC",
        progress_message = "Running DRC for {}".format(ctx.label.name),
    )
    return [DefaultInfo(files = depset([output]))]

kicad_drc = rule(
    implementation = _kicad_drc_impl,
    doc = "Run KiCad Design Rule Check and produce a JSON report.",
    attrs = {
        "src": attr.label(
            doc = "The .kicad_pcb file.",
            allow_single_file = [".kicad_pcb"],
            mandatory = True,
        ),
    },
)
