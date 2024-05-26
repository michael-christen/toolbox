import os
import sys

import pytest


def main():
    pytest_args = [
        "--ignore=external",
        "-p",
        "no:cacheprovider",
    ]

    # https://bazel.build/reference/test-encyclopedia
    test_tempdir = os.environ.get("TEST_TMPDIR", None)
    if test_tempdir:
        test_tempdir = os.path.join(
            os.path.abspath(test_tempdir), "pytest_temp"
        )
        pytest_args.append(f"--basetemp={test_tempdir}")

    # https://bazel.build/docs/user-manual#flag--test_filter
    # Take --test_filter options
    test_filter = os.environ.get("TESTBRIDGE_TEST_ONLY", None)
    if test_filter:
        pytest_args.extend(["-k", test_filter])

    # Invoke
    sys.exit(pytest.main(pytest_args + sys.argv[1:]))


if __name__ == '__main__':
    main()
