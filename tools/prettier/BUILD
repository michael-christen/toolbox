load("@npm//:prettier/package_json.bzl", prettier = "bin")

package(default_visibility = ["//visibility:private"])

prettier.prettier_binary(
    name = "prettier",
    # .prettierrc accessed directly not as (data)
    # Allow the binary to be run outside bazel
    env = {"BAZEL_BINDIR": "."},
)
