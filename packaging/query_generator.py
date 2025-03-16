"""Utility for generating source files based on bazel queries.

Cannot depend on any of our other sources, as this is one of a very small
amount of things that won't run with bazel.
"""

import argparse
import dataclasses
import difflib
import pathlib
import subprocess

_FIX_COMMAND = "./lint.sh --mode format"


@dataclasses.dataclass
class QueryFile:
    out_file: pathlib.Path
    variable_to_query: dict[str, str]


def _get_diff(a: str, b: str) -> str:
    """Get diff between two multi-line strings."""
    return "\n".join(
        list(difflib.Differ().compare(a.splitlines(), b.splitlines()))
    )


def generate(query_file: QueryFile, compare: bool) -> None:
    output_arr = [
        "# File generated via: query_generator.py",
        "#",
    ]
    for variable, query in sorted(query_file.variable_to_query.items()):
        targets = (
            subprocess.check_output(
                [
                    "bazel",
                    "query",
                    # Keep the output quiet
                    "--ui_event_filters=-info",
                    "--noshow_progress",
                    query,
                ]
            )
            .decode("utf-8")
            .strip()
            .splitlines()
        )
        output_arr.extend(
            [
                f"# {variable} generated via:",
                f"# `bazel query '{query}'`",
                f"{variable} = [",
            ]
            + [f'    "{t}",' for t in targets]
            + [
                "]",
                "",
            ]
        )
    output_msg = "\n".join(output_arr)
    if compare:
        if not query_file.out_file.exists():
            raise ValueError(f"{query_file.out_file} does not exist")
        current_msg = query_file.out_file.read_text()
        if output_msg != current_msg:
            diff = _get_diff(current_msg, output_msg)
            raise ValueError(
                f"{query_file.out_file} does not match generated content,"
                f" re-run '{_FIX_COMMAND}'. See diff:\n\n{diff}"
            )
        return
    else:
        query_file.out_file.write_text(output_msg)


def main(compare: bool) -> None:
    """Update or compare files generated via queries.

    Note that any file added here should have an entry in `.gitattributes`:
        packaging/generated.bzl linguist-generated=true
    This will prevent it from making the diffs too busy.
    """
    # NOTE: This must be called from the top-level directory
    QUERY_FILES = [
        QueryFile(
            out_file=pathlib.Path("packaging/generated.bzl"),
            variable_to_query={
                # target '//tools:_mypy_cli' is not visible, but gets included
                "PYTHON_TARGETS": (
                    'kind("py_binary", //...) + kind("py_library", //...)'
                    " - //tools:_mypy_cli"
                ),
                # Finds all proto_py_library (note that if someone decided to
                # name their python target similarly, we'd catch it too)
                "PROTO_PYTHON_TARGETS": (
                    'attr(name, "_py_library", //...)'
                    ' intersect kind("py_library", //...)'
                ),
            },
        ),
    ]
    for query_file in QUERY_FILES:
        generate(query_file, compare=compare)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some choices.")
    parser.add_argument(
        "--mode",
        choices=["check", "format"],
        help="Choose check/format from the given options",
        required=True,
    )
    args = parser.parse_args()
    if args.mode == "check":
        compare = True
    elif args.mode == "format":
        compare = False
    else:
        raise ValueError(f'"{args.mode}" is not a valid --mode')

    main(compare=compare)
