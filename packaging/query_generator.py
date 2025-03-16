"""Utility for generating source files based on bazel queries.

Cannot depend on any of our other sources, as this is one of a very small
amount of things that won't run with bazel.
"""

import argparse
import dataclasses
import pathlib
import subprocess


@dataclasses.dataclass
class QueryFile:
    out_file: pathlib.Path
    variable_name: str
    query: str


def generate(query_file: QueryFile, compare: bool) -> None:
    output_arr = []
    targets = (
        subprocess.check_output(
            [
                "bazel",
                "query",
                # Keep the output quiet
                "--ui_event_filters=-info",
                "--noshow_progress",
                query_file.query,
            ]
        )
        .decode("utf-8")
        .strip()
        .splitlines()
    )
    output_arr = (
        [
            "# Generated via:",
            f"# `bazel query '{query_file.query}'`",
            f"{query_file.variable_name} = [",
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
            # XXX: Show diff w/ difflib?
            # XXX: Instructions for how to fix
            raise ValueError(
                f"{query_file.out_file} does not match generated content"
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
    # XXX: Find the right location to call this from (ensure folks don't call
    # elsewhere)
    QUERY_FILES = [
        QueryFile(
            out_file=pathlib.Path("packaging/generated.bzl"),
            variable_name="PYTHON_TARGETS",
            # target '//tools:_mypy_cli' is not visible, but gets included
            query=(
                'kind("py_binary", //...) + kind("py_library", //...)'
                " - //tools:_mypy_cli"
            ),
        ),
        # XXX: Add just protos?
        # Finds all proto_py_library (note that if someone decided to name
        # their python target similarly, we'd catch it too)
        # bazel query \
        # attr(name, "_py_library", //...) intersect kind("py_library", //...)
    ]
    for query_file in QUERY_FILES:
        # XXX: Allow other generations to work if a single one fails?
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
