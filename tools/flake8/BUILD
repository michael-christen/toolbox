# https://rules-python.readthedocs.io/en/latest/api/rules_python/python/entry_points/py_console_script_binary.html
load("@rules_python//python/entry_points:py_console_script_binary.bzl", "py_console_script_binary")

package(default_visibility = ["//visibility:private"])

# Call with "-- `pwd`" may be the ticket?
py_console_script_binary(
    name = "flake8",
    data = ["//:.flake8"],
    pkg = "@pip//flake8",
    tags = [
        "no-mypy",
    ],
    visibility = ["//:__subpackages__"],
)
