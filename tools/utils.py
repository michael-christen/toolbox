import os
import sys


def update_argv_with_workspace():
    """If USE_TARGET_FROM_ENV is set, add BUILD_WORKSPACE_DIRECTORY to sys.argv

    https://bazel.build/docs/user-manual
    https://bazel.build/reference/be/make-variables

    Rules opt-in by setting the USE_TARGET_FROM_ENV env-var to a truthy
    statement.

    Raises if USE_TARGET_FROM_ENV is set and BUILD_WORKSPACE_DIRECTORY isn't.
    If USE_TARGET_FROM_ENV isn't set, does nothing.
    """
    if bool(os.environ.get("USE_TARGET_FROM_ENV", False)):
        # https://bazel.build/docs/user-manual
        # https://bazel.build/reference/be/make-variables
        target = os.environ.get("BUILD_WORKSPACE_DIRECTORY")
        if target is None:
            raise ValueError(
                "USE_TARGET_FROM_ENV set, but BUILD_WORKSPACE_DIRECTORY unset"
            )
        sys.argv.append(target)
