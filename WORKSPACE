# Set the name of the bazel workspace.
workspace(name = "mchristen")

# Repo description / layout
# | Repo                                               | bzlmod enabled |
# | ---                                                | ---            |
# | https://github.com/stackb/rules_proto              | NO             |
# | https://github.com/aspect-build/gcc-toolchain      | NO             |
# | https://github.com/bazelbuild/rules_python gazelle | YES, see #55   |
#
# Alternative to gcc-toolchain: https://github.com/uber/hermetic_cc_toolchain

# Load the http_archive rule so that we can have bazel download
# various rulesets and dependencies.
# The `load` statement imports the symbol for http_archive from the http.bzl
# file.  When the symbol is loaded you can use the rule.
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

http_archive(
    name = "build_stack_rules_proto",
    sha256 = "b7cbaf457d91e1d3c295df53b80f24e1d6da71c94ee61c42277ab938db6d1c68",
    strip_prefix = "rules_proto-3.2.0",
    urls = ["https://github.com/stackb/rules_proto/archive/v3.2.0.tar.gz"],
)

register_toolchains("@build_stack_rules_proto//toolchain:standard")

# Bring in @io_bazel_rules_go, @bazel_gazelle, @rules_proto if not already present
load("@build_stack_rules_proto//deps:core_deps.bzl", "core_deps")

core_deps()

load(
    "@io_bazel_rules_go//go:deps.bzl",
    "go_register_toolchains",
    "go_rules_dependencies",
)

go_rules_dependencies()

go_register_toolchains(version = "1.18.2")

load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")

gazelle_dependencies()

load("@build_stack_rules_proto//:go_deps.bzl", "gazelle_protobuf_extension_go_deps")

gazelle_protobuf_extension_go_deps()

load("@build_stack_rules_proto//deps:protobuf_core_deps.bzl", "protobuf_core_deps")

protobuf_core_deps()

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

# I added
load("@build_stack_rules_proto//deps:grpc_core_deps.bzl", "grpc_core_deps")

grpc_core_deps()

load(
    "@com_github_grpc_grpc//bazel:grpc_deps.bzl",
    "grpc_deps",
)

grpc_deps()

load("@com_google_googleapis//:repository_rules.bzl", "switched_rules_by_language")

# Initialize Google APIs with only C++ and Python targets
switched_rules_by_language(
    name = "com_google_googleapis_imports",
    cc = True,
    grpc = True,
    python = True,
)

load("@build_bazel_rules_apple//apple:repositories.bzl", "apple_rules_dependencies")

apple_rules_dependencies(ignore_version_differences = False)

# TODO(#78): Consider re-enabling
# http_archive(
#     name = "aspect_gcc_toolchain",
#     integrity = "sha256-iqcSkkfwbhKrNWeX957qE/I4fzKuj3GEB06OZAJ5Apk=",
#     strip_prefix = "gcc-toolchain-0.6.0",
#     urls = [
#         "https://github.com/f0rmiga/gcc-toolchain/archive/refs/tags/0.6.0.tar.gz",
#     ],
# )
#
# load("@aspect_gcc_toolchain//toolchain:repositories.bzl", "gcc_toolchain_dependencies")
#
# gcc_toolchain_dependencies()
#
# load("@aspect_gcc_toolchain//toolchain:defs.bzl", "ARCHS", "gcc_register_toolchain")
#
# gcc_register_toolchain(
#     name = "gcc_toolchain_x86_64",
#     target_arch = ARCHS.x86_64,
# )

# TODO: Should add buf too

# Remaining setup is for rules_python.

http_archive(
    name = "rules_python_gazelle_plugin",
    sha256 = "d71d2c67e0bce986e1c5a7731b4693226867c45bfe0b7c5e0067228a536fc580",
    strip_prefix = "rules_python-0.29.0/gazelle",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.29.0/rules_python-0.29.0.tar.gz",
)

# The rules_python gazelle extension has some third-party go dependencies
# which we need to fetch in order to compile it.
load("@rules_python_gazelle_plugin//:deps.bzl", _py_gazelle_deps = "gazelle_deps")

# See: https://github.com/bazelbuild/rules_python/blob/main/gazelle/README.md
# This rule loads and compiles various go dependencies that running gazelle
# for python requirements.
_py_gazelle_deps()


load(
    "@pigweed//pw_toolchain/rust:defs.bzl",
    "pw_rust_register_toolchain_and_target_repos",
    "pw_rust_register_toolchains",
)

pw_rust_register_toolchain_and_target_repos(
    cipd_tag = "rust_revision:bf9c7a64ad222b85397573668b39e6d1ab9f4a72",
)

# Allows creation of a `rust-project.json` file to allow rust analyzer to work.
load("@rules_rust//tools/rust_analyzer:deps.bzl", "rust_analyzer_dependencies")

rust_analyzer_dependencies()

pw_rust_register_toolchains()

# Vendored third party rust crates.
git_repository(
    name = "rust_crates",
    commit = "de54de1a2683212d8edb4e15ec7393eb013c849c",
    remote = "https://pigweed.googlesource.com/third_party/rust_crates",
)

# Registers platforms for use with toolchain resolution
register_execution_platforms("@local_config_platform//:host", "//platforms:all")
