# Set the name of the bazel workspace.
workspace(name = "mchristen")

# Load the http_archive rule so that we can have bazel download
# various rulesets and dependencies.
# The `load` statement imports the symbol for http_archive from the http.bzl
# file.  When the symbol is loaded you can use the rule.
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# XXX: Install the newest version once #1664 gets released to fix py_binary issues
http_archive(
    name = "rules_python",
    sha256 = "d70cd72a7a4880f0000a6346253414825c19cdd40a28289bdf67b8e6480edff8",
    strip_prefix = "rules_python-0.28.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.28.0/rules_python-0.28.0.tar.gz",
)

http_archive(
    name = "aspect_rules_py",
    sha256 = "50b4b43491cdfc13238c29cb159b7ccacf0a1e54bd27b65ff2d5fac69af4d46f",
    strip_prefix = "rules_py-0.4.0",
    url = "https://github.com/aspect-build/rules_py/releases/download/v0.4.0/rules_py-v0.4.0.tar.gz",
)
# Fetches the rules_py dependencies.
# (must come before aspect's gcc toolchain dependencies)
load("@aspect_rules_py//py:repositories.bzl", "rules_py_dependencies")
rules_py_dependencies()

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

load("@aspect_gcc_toolchain//toolchain:defs.bzl", "gcc_register_toolchain", "ARCHS")
gcc_register_toolchain(
    name = "gcc_toolchain_x86_64",
    target_arch = ARCHS.x86_64,
)


http_archive(
    name = "rules_rust",
    sha256 = "6357de5982dd32526e02278221bb8d6aa45717ba9bbacf43686b130aa2c72e1e",
    urls = ["https://github.com/bazelbuild/rules_rust/releases/download/0.30.0/rules_rust-v0.30.0.tar.gz"],
)

load("@rules_rust//rust:repositories.bzl", "rules_rust_dependencies", "rust_register_toolchains")

rules_rust_dependencies()

rust_register_toolchains(
  edition = "2021",
)

load("@rules_rust//crate_universe:repositories.bzl", "crate_universe_dependencies")

crate_universe_dependencies()

load("@rules_rust//crate_universe:defs.bzl", "crates_repository")

crates_repository(
    name = "crate_index",
    cargo_lockfile = "//:Cargo.lock",
    lockfile = "//:cargo-bazel-lock.json",
    manifests = [
        # "//:Cargo.toml",
        "//:examples/basic/Cargo.toml",
    ],
)

load("@crate_index//:defs.bzl", "crate_repositories")

crate_repositories()


http_archive(
    name = "com_google_protobuf",
    sha256 = "616bb3536ac1fff3fb1a141450fa28b875e985712170ea7f1bfe5e5fc41e2cd8",
    strip_prefix = "protobuf-24.4",
    urls = ["https://github.com/protocolbuffers/protobuf/archive/v24.4.tar.gz"],
)

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()
# XXX: Should add buf too

http_archive(
    name = "rules_proto",
    sha256 = "903af49528dc37ad2adbb744b317da520f133bc1cbbecbdd2a6c546c9ead080b",
    strip_prefix = "rules_proto-6.0.0-rc0",
    url = "https://github.com/bazelbuild/rules_proto/releases/download/6.0.0-rc0/rules_proto-6.0.0-rc0.tar.gz",
)

load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies", "rules_proto_toolchains")

rules_proto_dependencies()

rules_proto_toolchains()

# XXX: Example


######################################################################
# We need rules_go and bazel_gazelle, to build the gazelle plugin from source.
# Setup instructions for this section are at
# https://github.com/bazelbuild/bazel-gazelle#running-gazelle-with-bazel
# You may need to update the version of the rule, which is listed in the above
# documentation.
######################################################################

# Define an http_archive rule that will download the below ruleset,
# test the sha, and extract the ruleset to you local bazel cache.

http_archive(
    name = "io_bazel_rules_go",
    integrity = "sha256-fHbWI2so/2laoozzX5XeMXqUcv0fsUrHl8m/aE8Js3w=",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_go/releases/download/v0.44.2/rules_go-v0.44.2.zip",
        "https://github.com/bazelbuild/rules_go/releases/download/v0.44.2/rules_go-v0.44.2.zip",
    ],
)

http_archive(
    name = "bazel_gazelle",
    integrity = "sha256-MpOL2hbmcABjA1R5Bj2dJMYO2o15/Uc5Vj9Q0zHLMgk=",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-gazelle/releases/download/v0.35.0/bazel-gazelle-v0.35.0.tar.gz",
        "https://github.com/bazelbuild/bazel-gazelle/releases/download/v0.35.0/bazel-gazelle-v0.35.0.tar.gz",
    ],
)


# Load rules_go ruleset and expose the toolchain and dep rules.
load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", "go_rules_dependencies")
load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies", "go_repository")

############################################################
# Define your own dependencies here using go_repository.
# Else, dependencies declared by rules_go/gazelle will be used.
# The first declaration of an external repository "wins".
############################################################

# go_rules_dependencies is a function that registers external dependencies
# needed by the Go rules.
# See: https://github.com/bazelbuild/rules_go/blob/master/go/dependencies.rst#go_rules_dependencies
go_rules_dependencies()

# go_rules_dependencies is a function that registers external dependencies
# needed by the Go rules.
# See: https://github.com/bazelbuild/rules_go/blob/master/go/dependencies.rst#go_rules_dependencies
go_register_toolchains(version = "1.20.5")

# The following call configured the gazelle dependencies, Go environment and Go SDK.
gazelle_dependencies()

# Remaining setup is for rules_python.


http_archive(
    name = "rules_python_gazelle_plugin",
    sha256 = "d70cd72a7a4880f0000a6346253414825c19cdd40a28289bdf67b8e6480edff8",
    strip_prefix = "rules_python-0.28.0/gazelle",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.28.0/rules_python-0.28.0.tar.gz",
)

# Next we load the setup and toolchain from rules_python.
load("@rules_python//python:repositories.bzl", "py_repositories", "python_register_toolchains")

# Perform general setup
py_repositories()

# We now register a hermetic Python interpreter rather than relying on a system-installed interpreter.
# This toolchain will allow bazel to download a specific python version, and use that version
# for compilation.
python_register_toolchains(
    name = "python39",
    python_version = "3.9",
)

# load("@python39//:defs.bzl", "interpreter")

load("@rules_python//python:pip.bzl", "pip_parse")

# This macro wraps the `pip_repository` rule that invokes `pip`, with `incremental` set.
# Accepts a locked/compiled requirements file and installs the dependencies listed within.
# Those dependencies become available in a generated `requirements.bzl` file.
# You can instead check this `requirements.bzl` file into your repo.
pip_parse(
    name = "pip",
    # XXX: Use with compile_pip_requirements?
    requirements_lock = "//:requirements_lock.txt",
    # Here, we use the interpreter constant that resolves to the host interpreter from the default Python toolchain.
    # python_interpreter_target = interpreter,

    # # # Requirement groups allow Bazel to tolerate PyPi cycles by putting dependencies
    # # # which are known to form cycles into groups together.
    # # experimental_requirement_cycles = {
    # #     "sphinx": [
    # #         "sphinx",
    # #         "sphinxcontrib-qthelp",
    # #         "sphinxcontrib-htmlhelp",
    # #         "sphinxcontrib-devhelp",
    # #         "sphinxcontrib-applehelp",
    # #         "sphinxcontrib-serializinghtml",
    # #     ],
    # # },
    # # (Optional) You can provide a python_interpreter (path) or a python_interpreter_target (a Bazel target, that
    # # acts as an executable). The latter can be anything that could be used as Python interpreter. E.g.:
    # # 1. Python interpreter that you compile in the build file.
    # # 2. Pre-compiled python interpreter included with http_archive.
    # # 3. Wrapper script, like in the autodetecting python toolchain.
    # #
    # Set the location of the lock file.
)

# Load the install_deps macro.
load("@pip//:requirements.bzl", "install_deps")

# Initialize repositories for all packages in requirements_lock.txt.
install_deps()

# The rules_python gazelle extension has some third-party go dependencies
# which we need to fetch in order to compile it.
load("@rules_python_gazelle_plugin//:deps.bzl", _py_gazelle_deps = "gazelle_deps")

# See: https://github.com/bazelbuild/rules_python/blob/main/gazelle/README.md
# This rule loads and compiles various go dependencies that running gazelle
# for python requirements.
_py_gazelle_deps()
