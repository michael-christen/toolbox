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
        "hw_drivers",
        "hw_services",
        "mchristen",
        "third_party",
        "tools",
        "utils",
    ],
    deps = PYTHON_TARGETS,
)

py_wheel(
    name = "py_wheel_all",
    distribution = "mchristen_toolbox",
    python_tag = "py3",
    # Version comes from tools/workspace_status.sh when built with --stamp.
    # Dev builds (no --stamp) get the literal placeholder in the filename;
    # use the .dist target to get a wheel with the real stamped name.
    version = "{STABLE_GIT_VERSION}",
    stamp = -1,
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
