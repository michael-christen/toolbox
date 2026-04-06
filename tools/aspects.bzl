load("@pip_types//:types.bzl", "types")
load("@rules_mypy//mypy:mypy.bzl", "mypy")

mypy_aspect = mypy(
    mypy_cli = "@@//tools:mypy_cli",
    mypy_ini = "@@//:mypy.ini",
    types = types,
    suppression_tags = ["no-mypy"],
)
