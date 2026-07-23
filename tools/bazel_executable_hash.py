#!/usr/bin/env python3
"""
bazel_executable_hash.py

Given a list of Bazel executable targets, returns a map of target -> content hash
that reflects the full executable closure (binary + all runfiles content).

The hash covers:
  - The binary itself (via ExecutableSymlink action output)
  - All files in the runfiles tree (by dereferencing SourceSymlinkManifest entries)

Usage:
  python3 bazel_executable_hash.py //my/pkg:binary //other:tool
  python3 bazel_executable_hash.py --query 'attr("tags", "deliverable", //...)'
  python3 bazel_executable_hash.py --json //my/pkg:binary

Requires:
  - bazel (or bazelisk) on PATH
  - Targets must be buildable executables (go_binary, py_binary, cc_binary, etc.)
"""

import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


EXECUTABLE_HASH_VERSION = "1"  # bump if algorithm changes


def find_workspace_root() -> Path:
    """Walk up from cwd to find the Bazel workspace root."""
    cwd = Path.cwd()
    for directory in [cwd, *cwd.parents]:
        if (directory / "MODULE.bazel").exists() or (directory / "WORKSPACE").exists():
            return directory
    raise RuntimeError("Could not find Bazel workspace root from cwd")


def run_bazel(args: list[str], workspace: Path) -> subprocess.CompletedProcess:
    cmd = ["bazel"] + args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=workspace,
    )
    return result


def resolve_targets_from_query(query: str, workspace: Path) -> list[str]:
    """Expand a bazel query expression into a list of concrete target labels."""
    result = run_bazel(["query", query], workspace)
    if result.returncode != 0:
        raise RuntimeError(f"bazel query failed:\n{result.stderr}")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def get_action_outputs(targets: list[str], workspace: Path) -> dict[str, dict[str, str]]:
    """
    Run aquery for all targets at once and extract output paths for
    ExecutableSymlink and SourceSymlinkManifest actions per target.

    Returns: {target_label: {"binary": path, "manifest": path}}
    """
    # aquery with text output is easiest to parse without proto deps
    target_expr = " + ".join(f"deps({t}, 1)" for t in targets)
    # We only want actions directly on the target, not all deps
    aquery_expr = "mnemonic('ExecutableSymlink|SourceSymlinkManifest', {})".format(
        " + ".join(f"'{t}'" for t in targets)
    )

    result = run_bazel(
        [
            "aquery",
            "--output=jsonproto",
            "--include_commandline=false",
            "--nostamp",
            aquery_expr,
        ],
        workspace,
    )

    if result.returncode != 0:
        # Fall back to per-target if the union query fails
        raise RuntimeError(f"bazel aquery failed:\n{result.stderr.strip()}")

    data = json.loads(result.stdout)

    # Build artifact id -> path lookup
    artifact_map: dict[str, str] = {}
    for artifact in data.get("artifacts", []):
        artifact_map[artifact["id"]] = artifact.get("execPath", "")

    # Build target id -> label lookup
    target_map: dict[str, str] = {}
    for target in data.get("targets", []):
        target_map[target["id"]] = target.get("label", "")

    # Extract relevant actions grouped by target label
    results: dict[str, dict[str, str]] = {t: {} for t in targets}

    for action in data.get("actions", []):
        mnemonic = action.get("mnemonic", "")
        if mnemonic not in ("ExecutableSymlink", "SourceSymlinkManifest"):
            continue

        target_id = action.get("targetId")
        label = target_map.get(target_id, "")

        # Normalise label to match what the caller passed
        # (aquery may return canonical form like @@repo//pkg:name)
        canonical = label
        for requested in targets:
            if canonical.endswith(requested) or canonical == requested:
                label = requested
                break

        if label not in results:
            continue

        output_ids = action.get("outputIds", [])
        for oid in output_ids:
            path = artifact_map.get(oid, "")
            if mnemonic == "ExecutableSymlink":
                results[label]["binary"] = path
            elif mnemonic == "SourceSymlinkManifest":
                results[label]["manifest"] = path

    return results


def build_targets(targets: list[str], workspace: Path) -> None:
    """Build targets with --nostamp for reproducible outputs."""
    result = run_bazel(["build", "--nostamp"] + targets, workspace)
    if result.returncode != 0:
        raise RuntimeError(f"bazel build failed:\n{result.stderr.strip()}")


def hash_file_content(path: Path) -> bytes:
    """Return SHA-256 digest of a file's content."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.digest()


def compute_executable_hash(
    label: str,
    binary_exec_path: str,
    manifest_exec_path: str,
    workspace: Path,
    bazel_bin: Path,
) -> str:
    """
    Compute a stable content hash for an executable target.

    Algorithm:
      1. Hash the binary content (from ExecutableSymlink output)
      2. Parse the SourceSymlinkManifest and hash each listed file's content
      3. Sort the collected digests and combine into a final SHA-256
      4. Encode as base64url with 'h1:' prefix (Go dirhash convention)

    Logical paths are intentionally excluded — we only care whether the content
    of any file in the closure changed, not whether files were renamed (a rename
    without a content change wouldn't affect runtime behaviour, and any BUILD
    change that caused a rename would also change the binary or another file).

    Sorting the raw digest bytes gives a stable, order-independent result.
    """
    # Resolve exec paths relative to workspace (bazel-out symlink)
    def resolve(exec_path: str) -> Path:
        # Try bazel-out symlink first (works after build)
        p = workspace / exec_path
        if p.exists():
            return p
        # Try via bazel-bin for files under bin/
        p2 = bazel_bin / exec_path.replace("bazel-out/", "", 1).split("/", 2)[-1]
        if p2.exists():
            return p2
        raise FileNotFoundError(f"Cannot find built artifact: {exec_path}\n"
                                f"  Tried: {workspace / exec_path}")

    manifest_path = resolve(manifest_exec_path)
    binary_path = resolve(binary_exec_path)

    # Collect per-file SHA-256 digests
    digests: list[bytes] = []

    # 1. The binary itself
    digests.append(hash_file_content(binary_path))

    # 2. All files referenced in the runfiles manifest
    missing: list[str] = []
    with open(manifest_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(" ", 1)
            if len(parts) != 2:
                continue
            _, source_path = parts

            source = Path(source_path)
            if not source.exists():
                # Some entries may be empty-file sentinels or repo-level symlinks
                # that don't physically exist in all configurations — skip gracefully
                missing.append(source_path)
                continue

            if source.is_symlink():
                # Resolve symlink to get actual content
                source = source.resolve()

            if source.is_file():
                digests.append(hash_file_content(source))
            # Directories in manifests are unusual; skip them

    if missing:
        print(f"  [warn] {label}: {len(missing)} manifest entries not found on disk "
              f"(may be repo-level symlinks), skipping", file=sys.stderr)

    # 3. Sort digest bytes for a stable, order-independent combination
    digests.sort()

    final = hashlib.sha256()
    final.update(f"bazel-executable-hash:{EXECUTABLE_HASH_VERSION}\n".encode())
    for digest in digests:
        final.update(digest)

    digest = base64.urlsafe_b64encode(final.digest()).decode().rstrip("=")
    return f"h1:{digest}"


def get_bazel_bin(workspace: Path) -> Path:
    result = run_bazel(["info", "bazel-bin"], workspace)
    if result.returncode != 0:
        raise RuntimeError("Could not determine bazel-bin")
    return Path(result.stdout.strip())


def main():
    parser = argparse.ArgumentParser(
        description="Compute stable content hashes for Bazel executable targets."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Bazel target labels (e.g. //my/pkg:binary)",
    )
    parser.add_argument(
        "--query",
        metavar="EXPR",
        help="Bazel query expression to expand into targets (e.g. 'attr(\"tags\",\"deliverable\",//...)')",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--no-build",
        action="store_true",
        help="Skip bazel build (assumes outputs already exist)",
    )
    parser.add_argument(
        "--workspace",
        metavar="DIR",
        help="Path to Bazel workspace root (default: auto-detected from cwd)",
    )
    args = parser.parse_args()

    # Resolve workspace
    workspace = Path(args.workspace) if args.workspace else find_workspace_root()

    # Resolve targets
    targets: list[str] = list(args.targets)
    if args.query:
        print(f"Expanding query: {args.query}", file=sys.stderr)
        targets += resolve_targets_from_query(args.query, workspace)

    if not targets:
        parser.error("Provide at least one target label or --query expression")

    targets = list(dict.fromkeys(targets))  # deduplicate, preserve order
    print(f"Targets: {targets}", file=sys.stderr)

    # Build
    if not args.no_build:
        print("Building targets...", file=sys.stderr)
        build_targets(targets, workspace)

    # Get bazel-bin path
    bazel_bin = get_bazel_bin(workspace)

    # Get action outputs via aquery
    print("Querying action graph...", file=sys.stderr)
    action_outputs = get_action_outputs(targets, workspace)

    # Compute hashes
    results: dict[str, str] = {}
    errors: dict[str, str] = {}

    for target in targets:
        outputs = action_outputs.get(target, {})
        binary = outputs.get("binary")
        manifest = outputs.get("manifest")

        if not binary or not manifest:
            msg = (
                f"Could not find ExecutableSymlink and/or SourceSymlinkManifest "
                f"actions for {target}. Is it an executable target? "
                f"(found: {list(outputs.keys())})"
            )
            errors[target] = msg
            print(f"  [error] {target}: {msg}", file=sys.stderr)
            continue

        try:
            print(f"  Hashing {target}...", file=sys.stderr)
            h = compute_executable_hash(target, binary, manifest, workspace, bazel_bin)
            results[target] = h
        except Exception as e:
            errors[target] = str(e)
            print(f"  [error] {target}: {e}", file=sys.stderr)

    # Output
    if args.json_output:
        output = {"hashes": results, "errors": errors}
        print(json.dumps(output, indent=2))
    else:
        max_len = max((len(t) for t in results), default=0)
        for target, h in results.items():
            print(f"{target:<{max_len}}  {h}")
        if errors:
            print("\nErrors:", file=sys.stderr)
            for target, msg in errors.items():
                print(f"  {target}: {msg}", file=sys.stderr)

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
