"""Refreshes the Python "allowedVersions" allow-list in renovate.json.

Reads the rules_python version pinned in MODULE.bazel, fetches that
release's python/versions.bzl from GitHub, and intersects it with the
Python versions the pinned `pigweed` dep's `pigweed_python_packages` pip
hub actually publishes wheels for (fetched from that commit's own
MODULE.bazel) -- that hub only ever supports a handful of cpython minor
versions, and targets that pull deps like psutil/pyserial from it fail
to analyze on any Python version outside that set. The narrower of the
two constraints wins, and the result is written to the allowedVersions
regex for the "python toolchain version" packageRule so Renovate only
proposes bumping MODULE.bazel / tools/BUILD to a Python version both
rules_python and pigweed actually support.
"""

import base64
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
PIGWEED_MODULE_BAZEL_URL = (
    "https://pigweed.googlesource.com/pigweed/pigweed/+/"
    "{commit}/MODULE.bazel?format=TEXT"
)


def pinned_rules_python_version() -> str:
    match = re.search(
        r'bazel_dep\(name = "rules_python", version = "([^"]+)"\)',
        MODULE_BAZEL.read_text(),
    )
    if not match:
        sys.exit("could not find rules_python bazel_dep in MODULE.bazel")
    return match.group(1)


def pinned_pigweed_commit() -> str:
    match = re.search(
        r'git_override\(\s*module_name = "pigweed",.*?commit = "([0-9a-f]+)"',
        MODULE_BAZEL.read_text(),
        re.DOTALL,
    )
    if not match:
        sys.exit("could not find pigweed git_override in MODULE.bazel")
    return match.group(1)


def available_python_versions(rules_python_version: str) -> list[str]:
    url = VERSIONS_BZL_URL.format(version=rules_python_version)
    with urllib.request.urlopen(url) as response:
        text = response.read().decode()
    # TOOL_VERSIONS keys, e.g. `    "3.12.8": {`. Skip pre-releases
    # (e.g. "3.15.0a1") since those aren't valid pins.
    versions = re.findall(r'^ {4}"(\d+\.\d+\.\d+)":\s*\{', text, re.MULTILINE)
    return sorted(set(versions), key=lambda v: tuple(map(int, v.split("."))))


def pigweed_max_python_minor(pigweed_commit: str) -> tuple[int, int]:
    url = PIGWEED_MODULE_BAZEL_URL.format(commit=pigweed_commit)
    with urllib.request.urlopen(url) as response:
        text = base64.b64decode(response.read()).decode()
    # Each `pip.parse(... hub_name = "pigweed_python_packages", ...
    # python_version = "3.12", ...)` block declares one minor version
    # that hub publishes wheels for.
    minors: list[tuple[int, int]] = [
        (int(major), int(minor))
        for major, minor in (
            found.split(".")
            for found in re.findall(
                r'hub_name = "pigweed_python_packages",\s*'
                r'(?:.*\n)*?\s*python_version = "(\d+\.\d+)"',
                text,
            )
        )
    ]
    if not minors:
        sys.exit(
            "could not find any pigweed_python_packages python_version "
            f"entries in pigweed@{pigweed_commit}'s MODULE.bazel"
        )
    return max(minors)


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

    pigweed_commit = pinned_pigweed_commit()
    pigweed_max_minor = pigweed_max_python_minor(pigweed_commit)
    versions = [
        version
        for version in versions
        if tuple(map(int, version.split(".")))[:2] <= pigweed_max_minor
    ]
    if not versions:
        sys.exit(
            f"no Python versions are supported by both rules_python "
            f"{rules_python_version} and pigweed@{pigweed_commit} "
            f"(pigweed's pigweed_python_packages hub tops out at "
            f"{pigweed_max_minor[0]}.{pigweed_max_minor[1]})"
        )

    update_renovate_json(render_allowed_versions(versions))
    print(
        f"rules_python {rules_python_version}, pigweed@{pigweed_commit} "
        f"(max {pigweed_max_minor[0]}.{pigweed_max_minor[1]}): "
        f"{len(versions)} toolchain versions available, updated "
        f"allowedVersions in {RENOVATE_JSON}"
    )


if __name__ == "__main__":
    main()
