"""Tools for working with bazel.

```
bazel query //... --output proto > query_result.pb
# Load then operate on it
# For example
bazel query //... --output=proto |tee result.pb |bazel run //apps:bazel_parser
```
"""

import os
import pathlib
import subprocess

from third_party.bazel.src.main.protobuf import build_pb2


def get_workspace_directory() -> pathlib.Path:
    workspace = os.environ.get("BUILD_WORKING_DIRECTORY")
    assert workspace is not None
    return pathlib.Path(workspace)


def get_bazel_bin_directory() -> pathlib.Path:
    return pathlib.Path(
        subprocess.check_output(
            ["bazel", "info", "bazel-bin"], cwd=get_workspace_directory()
        )
        .decode("utf-8")
        .strip()
    )


def normalize_label(label: str) -> pathlib.Path:
    if label.startswith("//"):
        label = label[len("//") :]  # noqa: E203 whitespace conflict
    if label.startswith(":"):
        label = label[len(":") :]  # noqa: E203 whitespace conflict
    return pathlib.Path(label.replace(":", "/"))


def parse_build_output(query_bytes: bytes) -> build_pb2.QueryResult:
    result = build_pb2.QueryResult()
    result.ParseFromString(query_bytes)
    return result


def run_query(args: list[str]) -> build_pb2.QueryResult:
    all_args = ["bazel", "query", "--output=proto"] + args
    workspace_directory = get_workspace_directory()
    output = subprocess.check_output(all_args, cwd=workspace_directory)
    return parse_build_output(output)
