load("@rules_python//python:packaging.bzl", "py_package", "py_wheel")
load("//bzl:py.bzl", "py_binary")
load("//packaging:generated.bzl", "PYTHON_TARGETS")

package(default_visibility = ["//visibility:private"])

# https://rules-python.readthedocs.io/en/latest/api/rules_python/python/packaging.html#py_package
py_package(
    name = "py_package_all",
    # TODO(#203): Restructure repo so we don't need to update this
    packages = [
        "apps",
        "examples",
        "mchristen",
        "tools",
        "utils",
    ],
    deps = PYTHON_TARGETS,
)

py_wheel(
    name = "py_wheel_all",
    distribution = "mchristen_toolbox",
    python_tag = "py3",
    version = "0.0.0",
    deps = [":py_package_all"],
)

genrule(
    name = "py_wheel_all.reference",
    srcs = [":py_wheel_all"],
    outs = ["py_wheel_all.txt"],
    cmd = "echo $(location :py_wheel_all) >$@",
)

py_binary(
    name = "query_generator",
    srcs = ["query_generator.py"],
    visibility = ["//:__subpackages__"],
)
