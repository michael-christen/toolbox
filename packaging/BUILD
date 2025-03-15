load("//packaging:generated.bzl", "PYTHON_TARGETS")
load("@rules_python//python:packaging.bzl", "py_package", "py_wheel")
load("@aspect_rules_py//py:defs.bzl", "py_venv")

# https://rules-python.readthedocs.io/en/latest/api/rules_python/python/packaging.html#py_package
py_package(
    name = "py_package_all",
    # XXX: Do we need to name each of the packages used?
    packages = [
        "mchristen",
        "apps",
        "examples",
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

py_venv(
    name="py_venv_all",
    # XXX: Add all requirements
    deps = PYTHON_TARGETS,
    # XXX: error, warning, ignore
    # pick better / justify
    package_collisions = "ignore",
)
