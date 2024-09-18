import sys

from tools import bazel_utils


def main():
    """Oh to be, or not to be.

    That is the question.
    """
    query_result = bazel_utils.parse_build_output(sys.stdin.buffer.read())
    print(query_result)


if __name__ == "__main__":
    main()
