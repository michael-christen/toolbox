load("@npm//:pyright/package_json.bzl", pyright = "bin")

package(default_visibility = ["//visibility:private"])

pyright.pyright_binary(
    name = "pyright",
    # XXX: Needed?
    # Allow the binary to be run outside bazel
    env = {"BAZEL_BINDIR": "."},
)

