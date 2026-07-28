load("@npm//:renovate/package_json.bzl", renovate = "bin")
load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "sync_python_toolchain_versions",
    srcs = ["sync_python_toolchain_versions.py"],
    visibility = ["//:__subpackages__"],
)

renovate.renovate_binary(
    name = "renovate",
    # Renovate shells out to git directly; let it see the host's.
    env = {"BAZEL_BINDIR": "."},
    visibility = ["//:__subpackages__"],
)
