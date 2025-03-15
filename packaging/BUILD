load("//bzl:py.bzl", "py_binary")
load("@rules_python//python:packaging.bzl", "py_package", "py_wheel")
load("//packaging:generated.bzl", "PYTHON_TARGETS")

# https://rules-python.readthedocs.io/en/latest/api/rules_python/python/packaging.html#py_package
py_package(
    name = "py_package_all",
    # XXX: Do we need to name each of the packages used?
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

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "query_generator",
    srcs = ["query_generator.py"],
    visibility = ["//:__subpackages__"],
)
