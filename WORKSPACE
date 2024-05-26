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


http_archive(
    name = "mypy_integration",
    sha256 = "cf94c102fbaccb587eea8de5cf1cb7f55c5c74396a2468932c3a2a4df989aa1d",
    strip_prefix = "bazel-mypy-integration-0.4.0",
    url = "https://github.com/thundergolfer/bazel-mypy-integration/archive/refs/tags/0.4.0.tar.gz",
)

load(
    "@mypy_integration//repositories:repositories.bzl",
    mypy_integration_repositories = "repositories",
)
mypy_integration_repositories()

load("@mypy_integration//:config.bzl", "mypy_configuration")
# XXX: Optionally pass a MyPy config file, otherwise pass no argument.
mypy_configuration()

# XXX: Issue
# ± bazel build --@mypy_integration//:mypy=@pip//mypy:mypy //...                                                                                                                                                                                                                                                                                                                                                                      27s
# ERROR: Traceback (most recent call last):
#         File "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/mypy_integration/repositories/py_repositories.bzl", line 6, column 40, in <toplevel>
#                 load("@rules_python//python:pip.bzl", "pip_install")
# Error: file '@rules_python//python:pip.bzl' does not contain symbol 'pip_install'
# ERROR: Error computing the main repository mapping: at /home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/mypy_integration/repositories/deps.bzl:7:6: initialization of module 'repositories/py_repositories.bzl' failed
# 
# load("@mypy_integration//repositories:deps.bzl", mypy_integration_deps = "deps")

# mypy_integration_deps(
#     mypy_requirements_file="//:requirements_lock.txt",
#     # XXX: Needed?
#     # python_interpreter = "python3.9"  # /home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:/home/runner/.local/bin:/opt/pipx_bin:/home/runner/.cargo/bin:/home/runner/.config/composer/vendor/bin:/usr/local/.ghcup/bin:/home/runner/.dotnet/tools:/snap/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin is searched for exe.
#     # OR
#     # python_interpreter_target = "@python3_interpreter//:bin/python3",
# )
