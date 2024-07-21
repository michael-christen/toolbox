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

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

# Load the http_archive rule so that we can have bazel download
# various rulesets and dependencies.
# The `load` statement imports the symbol for http_archive from the http.bzl
# file.  When the symbol is loaded you can use the rule.
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "build_stack_rules_proto",
    sha256 = "ee7a11d66e7bbc5b0f7a35ca3e960cb9a5f8a314b22252e19912dfbc6e22782d",
    strip_prefix = "rules_proto-3.1.0",
    urls = ["https://github.com/stackb/rules_proto/archive/v3.1.0.tar.gz"],
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

http_archive(
    name = "aspect_gcc_toolchain",
    sha256 = "3341394b1376fb96a87ac3ca01c582f7f18e7dc5e16e8cf40880a31dd7ac0e1e",
    strip_prefix = "gcc-toolchain-0.4.2",
    urls = [
        "https://github.com/aspect-build/gcc-toolchain/archive/refs/tags/0.4.2.tar.gz",
    ],
)

load("@aspect_gcc_toolchain//toolchain:repositories.bzl", "gcc_toolchain_dependencies")

gcc_toolchain_dependencies()

load("@aspect_gcc_toolchain//toolchain:defs.bzl", "ARCHS", "gcc_register_toolchain")

gcc_register_toolchain(
    name = "gcc_toolchain_x86_64",
    target_arch = ARCHS.x86_64,
)

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

git_repository(
    name = "pigweed",
    commit = "c00e9e430addee0c8add16c32eb6d8ab94189b9e",
    remote = "https://pigweed.googlesource.com/pigweed/pigweed.git",
)
