# Set the name of the bazel workspace.
workspace(name = "mchristen")

# Load the http_archive rule so that we can have bazel download
# various rulesets and dependencies.
# The `load` statement imports the symbol for http_archive from the http.bzl
# file.  When the symbol is loaded you can use the rule.
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "d71d2c67e0bce986e1c5a7731b4693226867c45bfe0b7c5e0067228a536fc580",
    strip_prefix = "rules_python-0.29.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.29.0/rules_python-0.29.0.tar.gz",
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

# XXX: Intefering with rules_rust ...
# ERROR: /home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rules_rust/util/process_wrapper/BUILD.bazel:31:36: Compiling Rust (without process_wrapper) bin process_wrapper (6 fi
# les) [for tool] failed: (Exit 1): process_wrapper.sh failed: error executing command (from target @rules_rust//util/process_wrapper:process_wrapper) bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/pro
# cess_wrapper/process_wrapper.sh -- ... (remaining 21 arguments skipped)                                   
#                                                                                                           
# Use --sandbox_debug to see verbose messages from the sandbox and retain the sandbox build root for debugging                                                                                                        
# error: linking with `external/gcc_toolchain_x86_64/bin/gcc` failed: exit status: 127                                                                                                                                
#   = note: LC_ALL="C" PATH="/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/bi
# n" VSLANG="1033" "external/gcc_toolchain_x86_64/bin/gcc" "-m64" "/tmp/rustccSpiSS/symbols.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a6
# 2c4dab-cgu.00.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.01.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rule
# s_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.02.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62
# c4dab-cgu.03.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.04.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules
# _rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.05.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c
# 4dab-cgu.06.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.07.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_
# rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.08.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4
# dab-cgu.09.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.10.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_r
# ust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.11.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4d
# ab-cgu.12.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.13.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_ru
# st/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.14.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4da
# b-cgu.15.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.gkf5n1p5osl7kwu.rcgu.o" "-Wl,--as-needed" "-L" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rust_linux
# _x86_64__x86_64-unknown-linux-gnu__stable_tools/rust_toolchain/lib/rustlib/x86_64-unknown-linux-gnu/lib" "-L" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust_tinyjson" "-L" "/home/mchristen/.cache/bazel/_
# bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib" "-Wl,-Bstatic" "/home/mchristen/.cache/bazel/_bazel_mc
# hristen/eabc9c58e7a2790b61df5bad4df6e1e8/execroot/mchristen/bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust_tinyjson/libtinyjson-4031717389.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2
# 790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libstd-6498d8891e016dca.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c
# 58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libpanic_unwind-3debdee1a9058d84.rlib" "/home/mchristen/.cache/bazel/_bazel_m
# christen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libobject-8339c5bd5cbc92bf.rlib" "/home/mchristen/.cache/bazel
# /_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libmemchr-160ebcebb54c11ba.rlib" "/home/mchristen/.ca
# che/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libaddr2line-95c75789f1b65e37.rlib" "/home/m
# christen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libgimli-7e8094f2d6258832.rlib" 
# "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/librustc_demangle-bac978
# 3ef1b45db0.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libstd_
# detect-a1cd87df2f2d8e76.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gn
# u/lib/libhashbrown-7fd06d468d7dba16.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unkn
# own-linux-gnu/lib/librustc_std_workspace_alloc-5ac19487656e05bf.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_t
# ools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libminiz_oxide-c7c35d32cf825c11.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux
# -gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libadler-c523f1571362e70b.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unkno
# wn-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libunwind-85f17c92b770a911.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86
# _64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libcfg_if-598d3ba148dadcea.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x8
# 6_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/liblibc-a58ec2dab545caa4.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_l
# inux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/liballoc-f9dda8cca149f0fc.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/externa
# l/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/librustc_std_workspace_core-7ba4c315dd7a3503.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a27
# 90b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libcore-5ac2993e19124966.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c
# 58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libcompiler_builtins-df2fb7f50dec519a.rlib" "-Wl,-Bdynamic" "-lgcc_s" "-lutil
# " "-lrt" "-lpthread" "-lm" "-ldl" "-lc" "-Wl,--eh-frame-hdr" "-Wl,-z,noexecstack" "-L" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-li
# nux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib" "-o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper" "-Wl,--gc-sections" "-pie" "-Wl,-z,relro,-z,now" 
# "-Wl,-O1" "-Wl,--strip-debug" "-nodefaultlibs" "-ldl" "-lpthread" "-Wl,-z,relro,-z,now" "-pass-exit-codes" "-lm" "-lstdc++" "-Wl,--gc-sections" "--sysroot" "external/sysroot_x86_64" "-Bexternal/gcc_toolchain_x86_
# 64/bin" "-Bexternal/sysroot_x86_64//usr/lib" "-Bexternal/sysroot_x86_64//lib64" "-Lexternal/sysroot_x86_64//lib64" "-Lexternal/sysroot_x86_64//usr/lib" "-Lexternal/sysroot_x86_64//lib/gcc/x86_64-linux/10.3.0"    
#   = note: external/gcc_toolchain_x86_64/bin/gcc: line 24: realpath: command not found                     
#           external/gcc_toolchain_x86_64/bin/gcc: line 24: dirname: command not found                                                                                                                                
#           external/gcc_toolchain_x86_64/bin/gcc: line 24: realpath: command not found

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

http_archive(
    name = "rules_rust",
    integrity = "sha256-ZQGWDD5NoySV0eEAfe0HaaU0yxlcMN6jaqVPnYo/A2E=",
    urls = ["https://github.com/bazelbuild/rules_rust/releases/download/0.38.0/rules_rust-v0.38.0.tar.gz"],
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
# TODO: Should add buf too

http_archive(
    name = "rules_proto",
    sha256 = "903af49528dc37ad2adbb744b317da520f133bc1cbbecbdd2a6c546c9ead080b",
    strip_prefix = "rules_proto-6.0.0-rc0",
    url = "https://github.com/bazelbuild/rules_proto/releases/download/6.0.0-rc0/rules_proto-6.0.0-rc0.tar.gz",
)

load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies", "rules_proto_toolchains")

rules_proto_dependencies()

rules_proto_toolchains()

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
    sha256 = "d3fa66a39028e97d76f9e2db8f1b0c11c099e8e01bf363a923074784e451f809",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-gazelle/releases/download/v0.33.0/bazel-gazelle-v0.33.0.tar.gz",
        "https://github.com/bazelbuild/bazel-gazelle/releases/download/v0.33.0/bazel-gazelle-v0.33.0.tar.gz",
    ],
)

# Load rules_go ruleset and expose the toolchain and dep rules.
load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", "go_rules_dependencies")
load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")

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
    sha256 = "d71d2c67e0bce986e1c5a7731b4693226867c45bfe0b7c5e0067228a536fc580",
    strip_prefix = "rules_python-0.29.0/gazelle",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.29.0/rules_python-0.29.0.tar.gz",
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

load("@python39//:defs.bzl", "interpreter")
load("@rules_python//python:pip.bzl", "pip_parse")

# This macro wraps the `pip_repository` rule that invokes `pip`, with `incremental` set.
# Accepts a locked/compiled requirements file and installs the dependencies listed within.
# Those dependencies become available in a generated `requirements.bzl` file.
# You can instead check this `requirements.bzl` file into your repo.
pip_parse(
    name = "pip",
    # (Optional) You can provide a python_interpreter (path) or a python_interpreter_target (a Bazel target, that
    # acts as an executable). The latter can be anything that could be used as Python interpreter. E.g.:
    # 1. Python interpreter that you compile in the build file.
    # 2. Pre-compiled python interpreter included with http_archive.
    # 3. Wrapper script, like in the autodetecting python toolchain.
    # Here, we use the interpreter constant that resolves to the host interpreter from the default Python toolchain.
    python_interpreter_target = interpreter,
    # Set the location of the lock file.
    requirements_lock = "//:requirements_lock.txt",
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

# Load stackb/rules_proto
http_archive(
    name = "build_stack_rules_proto",
    sha256 = "ac7e2966a78660e83e1ba84a06db6eda9a7659a841b6a7fd93028cd8757afbfb",
    strip_prefix = "rules_proto-2.0.1",
    urls = ["https://github.com/stackb/rules_proto/archive/v2.0.1.tar.gz"],
)

register_toolchains("@build_stack_rules_proto//toolchain:standard")

# Bring in @io_bazel_rules_go, @bazel_gazelle, @rules_proto if not already present
load("@build_stack_rules_proto//deps:core_deps.bzl", "core_deps")

core_deps()

load("@build_stack_rules_proto//:go_deps.bzl", "gazelle_protobuf_extension_go_deps")

gazelle_protobuf_extension_go_deps()

load("@build_stack_rules_proto//deps:protobuf_core_deps.bzl", "protobuf_core_deps")

protobuf_core_deps()

http_archive(
    name = "com_github_bazelbuild_buildtools",
    sha256 = "ae34c344514e08c23e90da0e2d6cb700fcd28e80c02e23e4d5715dddcb42f7b3",
    strip_prefix = "buildtools-4.2.2",
    urls = [
        "https://github.com/bazelbuild/buildtools/archive/refs/tags/4.2.2.tar.gz",
    ],
)
