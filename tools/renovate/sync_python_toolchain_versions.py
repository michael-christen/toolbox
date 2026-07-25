"""Refreshes the Python "allowedVersions" allow-list in renovate.json.

Reads the rules_python version pinned in MODULE.bazel, fetches that
release's python/versions.bzl from GitHub, and rewrites the
allowedVersions regex for the "python toolchain version" packageRule so
Renovate only ever proposes bumping MODULE.bazel / tools/BUILD to a
Python version rules_python actually has a prebuilt toolchain for.
"""

import re
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_BAZEL = REPO_ROOT / "MODULE.bazel"
RENOVATE_JSON = REPO_ROOT / ".github/renovate.json"

VERSIONS_BZL_URL = (
    "https://raw.githubusercontent.com/bazelbuild/rules_python/"
    "{version}/python/versions.bzl"
)


def pinned_rules_python_version() -> str:
    match = re.search(
        r'bazel_dep\(name = "rules_python", version = "([^"]+)"\)',
        MODULE_BAZEL.read_text(),
    )
    if not match:
        sys.exit("could not find rules_python bazel_dep in MODULE.bazel")
    return match.group(1)


def available_python_versions(rules_python_version: str) -> list[str]:
    url = VERSIONS_BZL_URL.format(version=rules_python_version)
    with urllib.request.urlopen(url) as response:
        text = response.read().decode()
    # TOOL_VERSIONS keys, e.g. `    "3.12.8": {`. Skip pre-releases
    # (e.g. "3.15.0a1") since those aren't valid pins.
    versions = re.findall(r'^ {4}"(\d+\.\d+\.\d+)":\s*\{', text, re.MULTILINE)
    return sorted(set(versions), key=lambda v: tuple(map(int, v.split("."))))


def render_allowed_versions(versions: list[str]) -> str:
    escaped = "|".join(re.escape(version) for version in versions)
    regex = f"/^({escaped})$/"
    # Double backslashes so the regex survives as a JSON string literal.
    return regex.replace("\\", "\\\\")


def update_renovate_json(allowed_versions: str) -> None:
    text = RENOVATE_JSON.read_text()
    pattern = re.compile(
        r'("groupName": "python toolchain version".*?"allowedVersions": ")'
        r'[^"]*(")',
        re.DOTALL,
    )
    new_text, count = pattern.subn(
        lambda m: m.group(1) + allowed_versions + m.group(2), text
    )
    if count != 1:
        sys.exit(
            "expected exactly one 'python toolchain version' packageRule "
            f"with an allowedVersions field, found {count}"
        )
    RENOVATE_JSON.write_text(new_text)


def main() -> None:
    rules_python_version = pinned_rules_python_version()
    versions = available_python_versions(rules_python_version)
    if not versions:
        sys.exit(
            f"no Python toolchain versions found for rules_python "
            f"{rules_python_version}"
        )
    update_renovate_json(render_allowed_versions(versions))
    print(
        f"rules_python {rules_python_version}: {len(versions)} toolchain "
        f"versions available, updated allowedVersions in {RENOVATE_JSON}"
    )


if __name__ == "__main__":
    main()
