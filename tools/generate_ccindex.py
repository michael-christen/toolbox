"""Generate ccindex files for gazelle_cc header-to-target resolution.

Generates:
  tools/pigweed.ccindex  - @pigweed//pw_* cc_library header -> target mappings
  tools/emboss.ccindex   - Local emboss_cc_library header -> target mappings
  tools/nanopb.ccindex   - Local nanopb_proto_library header -> target mappings

Must be run from the repo root (cannot use bazel run due to nested
invocation constraints -- see TODO(#205) in lint.sh for context).

Usage:
    python tools/generate_ccindex.py --mode format  # regenerate
    python tools/generate_ccindex.py --mode check   # verify up to date

lint.sh calls this automatically.
"""

import argparse
import difflib
import json
import pathlib
import subprocess

from third_party.bazel.src.main.protobuf import build_pb2

FIX_COMMAND = "./lint.sh --mode format"
PIGWEED_CCINDEX = pathlib.Path("tools/pigweed.ccindex")
EMBOSS_CCINDEX = pathlib.Path("tools/emboss.ccindex")
NANOPB_CCINDEX = pathlib.Path("tools/nanopb.ccindex")


def _run_query(query: str) -> list[build_pb2.Target]:
    """Run a bazel query and return the targets as proto Target messages."""
    # --keep_going tolerates packages with missing external deps (exit 2/3).
    proc = subprocess.run(
        [
            "bazel",
            "query",
            "--ui_event_filters=-info",
            "--noshow_progress",
            "--keep_going",
            "--output=proto",
            query,
        ],
        capture_output=True,
    )
    if proc.returncode not in (0, 2, 3) or not proc.stdout:
        raise RuntimeError(
            f"bazel query failed (exit {proc.returncode}):\n"
            f"{proc.stderr.decode()}"
        )
    result = build_pb2.QueryResult()
    result.ParseFromString(proc.stdout)
    return list(result.target)


def _attr(rule: build_pb2.Rule, name: str) -> str:
    for attr in rule.attribute:
        if attr.name == name:
            return attr.string_value
    return ""


def _attr_list(rule: build_pb2.Rule, name: str) -> list[str]:
    for attr in rule.attribute:
        if attr.name == name:
            return list(attr.string_list_value)
    return []


def _file_in_pkg(label: str) -> str | None:
    """'@pigweed//pw_i2c:public/pw_i2c/reg.h' -> 'public/pw_i2c/reg.h'"""
    return label.split(":", 1)[1] if ":" in label else None


def _package_of(label: str) -> str:
    """'//hw_drivers/lis3mdl:lis3mdl_emb_ir' -> 'hw_drivers/lis3mdl'"""
    return label.split("//", 1)[1].split(":")[0]


def _effective_include_path(path: str, strip: str, add: str) -> str:
    if strip:
        s = strip.lstrip("/")
        if path.startswith(s + "/"):
            path = path[len(s) + 1 :]  # noqa: E203
        elif path == s:
            return ""
    if add:
        path = add.strip("/") + "/" + path
    return path


def generate_pigweed_index() -> dict[str, str]:
    """Build header->target mapping for @pigweed//pw_* cc_library targets.

    Queries only Pigweed targets reachable from our code to avoid traversing
    Pigweed packages that have missing external deps (doxygen, rules_mypy,
    etc). filter() matches against the bzlmod canonical name which
    contains 'pigweed+'.
    Entries with multiple providers are omitted; use # gazelle:resolve
    instead.
    """
    targets = _run_query('filter("pigweed[+]", kind(cc_library, deps(//...)))')
    index: dict[str, list[str]] = {}

    for t in targets:
        if t.type != build_pb2.Target.RULE:
            continue
        rule = t.rule
        if rule.rule_class != "cc_library":
            continue

        hdrs = _attr_list(rule, "hdrs")
        if not hdrs:
            continue

        strip = _attr(rule, "strip_include_prefix")
        add = _attr(rule, "include_prefix")
        label = rule.name

        for hdr in hdrs:
            f = _file_in_pkg(hdr)
            if not f or not (f.endswith(".h") or f.endswith(".hpp")):
                continue
            include_path = _effective_include_path(f, strip, add)
            if not include_path:
                continue
            index.setdefault(include_path, [])
            if label not in index[include_path]:
                index[include_path].append(label)

    return {k: v[0] for k, v in sorted(index.items()) if len(v) == 1}


def generate_emboss_index() -> dict[str, str]:
    """Build header->target mapping for local emboss_cc_library targets.

    emboss_cc_library(name = "foo_emb", srcs = ["foo.emb"]) in package
    //pkg generates foo.emb.h, included as pkg/foo.emb.h.
    The emboss_library rule (foo_emb_ir) carries the srcs; generator_name
    points back to the cc target (foo_emb) that callers should depend on.
    """
    targets = _run_query("kind(emboss_library, //...)")
    index: dict[str, str] = {}

    for t in targets:
        if t.type != build_pb2.Target.RULE:
            continue
        rule = t.rule

        srcs = _attr_list(rule, "srcs")
        generator_name = _attr(rule, "generator_name")
        if not srcs or not generator_name:
            continue

        package = _package_of(rule.name)
        for src in srcs:
            f = _file_in_pkg(src)
            if not f or not f.endswith(".emb"):
                continue
            include_path = f"{package}/{f}.h"
            index[include_path] = f"//{package}:{generator_name}"

    return dict(sorted(index.items()))


def generate_nanopb_index() -> dict[str, str]:
    """Build header->target mapping for local nanopb_proto_library targets.

    nanopb_proto_library(name = "foo_nanopb", deps = [":foo_proto"]) in
    package //pkg generates foo.pb.h, included as pkg/foo.pb.h.
    """
    nanopb_targets = _run_query("kind(nanopb_proto_library, //...)")
    proto_targets = _run_query(
        "kind(proto_library, deps(kind(nanopb_proto_library, //...)))"
    )

    # Build map from proto_library label -> list of .proto source filenames
    proto_srcs: dict[str, list[str]] = {}
    for t in proto_targets:
        if t.type != build_pb2.Target.RULE:
            continue
        rule = t.rule
        srcs = _attr_list(rule, "srcs")
        proto_srcs[rule.name] = srcs

    index: dict[str, str] = {}
    for t in nanopb_targets:
        if t.type != build_pb2.Target.RULE:
            continue
        rule = t.rule
        nanopb_label = rule.name
        package = _package_of(nanopb_label)

        for proto_dep in _attr_list(rule, "protos"):
            for src in proto_srcs.get(proto_dep, []):
                f = _file_in_pkg(src)
                if not f or not f.endswith(".proto"):
                    continue
                stem = f[: -len(".proto")]
                include_path = f"{package}/{stem}.pb.h"
                index[include_path] = nanopb_label

    return dict(sorted(index.items()))


def _to_json(index: dict) -> str:
    return json.dumps(index, indent=2, sort_keys=True) + "\n"


def _check_or_write(path: pathlib.Path, content: str, mode: str) -> None:
    if mode == "format":
        path.write_text(content)
        print(f"Updated {path}")
    else:
        if not path.exists():
            raise SystemExit(
                f"Error: {path} does not exist. "
                f"Run '{FIX_COMMAND}' to generate."
            )
        current = path.read_text()
        if content == current:
            return
        diff = "\n".join(
            difflib.unified_diff(
                current.splitlines(),
                content.splitlines(),
                fromfile=str(path),
                tofile="(generated)",
                lineterm="",  # noqa: E501
            )
        )
        raise SystemExit(
            f"{path} is out of date. Run '{FIX_COMMAND}' to update.\n\n{diff}"
        )


def main(mode: str) -> None:
    _check_or_write(PIGWEED_CCINDEX, _to_json(generate_pigweed_index()), mode)
    _check_or_write(EMBOSS_CCINDEX, _to_json(generate_emboss_index()), mode)
    _check_or_write(NANOPB_CCINDEX, _to_json(generate_nanopb_index()), mode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["check", "format"], required=True)
    args = parser.parse_args()
    main(args.mode)
