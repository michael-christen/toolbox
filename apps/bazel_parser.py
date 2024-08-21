import sys

from tools import bazel_utils


def main():
    # query_result = bazel_utils.parse_build_output(sys.stdin.buffer.read())
    # print(query_result)
    event = bazel_utils.parse_build_event(sys.stdin.buffer.read())
    print(event)


if __name__ == "__main__":
    main()
