"""Module docstring."""
import sys

from tools import bazel_utils


def main():
    """Read stdin to parse build output."""
    query_result = bazel_utils.parse_build_output(sys.stdin.buffer.read())
    print(query_result)


if __name__ == "__main__":
    main()
