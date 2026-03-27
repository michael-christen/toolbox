"""Generate ccindex files for gazelle_cc header-to-target resolution.

Generates:
  pigweed.ccindex  - @pigweed//pw_* cc_library header -> target mappings
  emboss.ccindex   - Local emboss_cc_library header -> target mappings

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

FIX_COMMAND = "./lint.sh --mode format"
PIGWEED_CCINDEX = pathlib.Path("tools/pigweed.ccindex")
EMBOSS_CCINDEX = pathlib.Path("tools/emboss.ccindex")


def _run_query(query: str) -> list[dict]:
    """Run a bazel query and return the targets as parsed JSON dicts."""
    # --keep_going tolerates packages with missing external deps (exit 2).
    # streamed_jsonproto emits one JSON object per line, each wrapping one target.
    proc = subprocess.run(
        [
            "bazel",
            "query",
            "--ui_event_filters=-info",
            "--noshow_progress",
            "--keep_going",
            "--output=streamed_jsonproto",
            query,
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode not in (0, 2, 3) or not proc.stdout.strip():
        raise RuntimeError(
            f"bazel query failed (exit {proc.returncode}):\n{proc.stderr}"
        )
    targets = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line:
            targets.append(json.loads(line))
    return targets


def _attr(rule: dict, name: str) -> str:
    for attr in rule.get("attribute", []):
        if attr.get("name") == name:
            return attr.get("stringValue", "")
    return ""


def _attr_list(rule: dict, name: str) -> list[str]:
    for attr in rule.get("attribute", []):
        if attr.get("name") == name:
            return attr.get("stringListValue", [])
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
            path = path[len(s) + 1 :]
        elif path == s:
            return ""
    if add:
        path = add.strip("/") + "/" + path
    return path


def generate_pigweed_index() -> dict[str, str | list[str]]:
    """Build header->target mapping for @pigweed//pw_* cc_library targets.

    Queries only Pigweed targets reachable from our code to avoid traversing
    Pigweed packages that have missing external deps (doxygen, rules_mypy, etc).
    filter() matches against the bzlmod canonical name which contains 'pigweed+'.
    """
    targets = _run_query(
        'filter("pigweed[+]", kind(cc_library, deps(//...)))'
    )
    index: dict[str, list[str]] = {}

    for t in targets:
        if t.get("type") != "RULE":
            continue
        rule = t["rule"]
        if rule.get("ruleClass") != "cc_library":
            continue

        hdrs = _attr_list(rule, "hdrs")
        if not hdrs:
            continue

        strip = _attr(rule, "strip_include_prefix")
        add = _attr(rule, "include_prefix")
        label = rule["name"]

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

    return {
        k: v[0]
        for k, v in sorted(index.items())
        if len(v) == 1
    }


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
        if t.get("type") != "RULE":
            continue
        rule = t["rule"]

        srcs = _attr_list(rule, "srcs")
        generator_name = _attr(rule, "generator_name")
        if not srcs or not generator_name:
            continue

        package = _package_of(rule["name"])
        for src in srcs:
            f = _file_in_pkg(src)
            if not f or not f.endswith(".emb"):
                continue
            include_path = f"{package}/{f}.h"
            index[include_path] = f"//{package}:{generator_name}"

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
                f"Error: {path} does not exist. Run '{FIX_COMMAND}' to generate."
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
                lineterm="",
            )
        )
        raise SystemExit(
            f"{path} is out of date. Run '{FIX_COMMAND}' to update.\n\n{diff}"
        )


def main(mode: str) -> None:
    _check_or_write(PIGWEED_CCINDEX, _to_json(generate_pigweed_index()), mode)
    _check_or_write(EMBOSS_CCINDEX, _to_json(generate_emboss_index()), mode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["check", "format"], required=True)
    args = parser.parse_args()
    main(args.mode)
