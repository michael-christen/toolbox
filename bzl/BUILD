load("//bzl:py.bzl", "py_binary")

exports_files([
    "pytest_main.py",
])

py_binary(
    name = "pytest_main",
    srcs = ["pytest_main.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//pytest"],
)

sh_binary(
    name = "bin_size",
    srcs = ["bin_size.sh"],
    visibility = ["//:__subpackages__"],
)
