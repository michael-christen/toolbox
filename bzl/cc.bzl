# Custom macros of common cc rules to enable common modifications
#
# See https://bazel.build/reference/be/c-cpp for documentation
#
# We define our copts in this manner, rather than in .bazelrc to avoid
# modifying how 3rd party C++ is compiled
#
# We have a separate c_binary/c_library defined as a quick work around to give
# similar resolution of using different copts based on language. Here is how
# bazel does this internally with command line arguments
# https://github.com/bazelbuild/bazel/blob/300c5867b7d2da1ba32abc20e95662096c2a7a08/src/main/java/com/google/devtools/build/lib/rules/cpp/CcCompilationHelper.java#L1244-L1269
# We could make some more clever rules to do this automatically, but the amount
# of .c code I write is so miniscule, this shouldn't really be a problem.
#
# Note, an alternative would be to modify the cc_toolchain with features, see
# https://bazel.build/tutorials/ccp-toolchain-config for more info.
#
# If you want to use custom COPTS, then just use @rules_cc//cc:defs.bzl
# directly and include all of the pieces you want
load("@rules_cc//cc:defs.bzl", _cc_binary = "cc_binary", _cc_library = "cc_library", _cc_test = "cc_test")

# C Compiler Options: https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html

COPTS = [
    # All Warnings and then some, mark em as errors too
    "-Wall",
    # Warnings are errors
    "-Werror",
    # -Wextra, with a few exceptions
    "-Wmemset-transposed-args",
    "-Wcast-function-type",
    "-Wclobbered",
    "-Wempty-body",
    "-Wenum-conversion",
    "-Wexpansion-to-defined",
    "-Wignored-qualifiers",
    "-Wimplicit-fallthrough=3",
    "-Wmaybe-uninitialized",
    "-Wshift-negative-value",
    "-Wsign-compare",
    "-Wstring-compare",
    "-Wtype-limits",
    "-Wuninitialized",
    "-Wunused-but-set-parameter",
    "-Wmissing-field-initializers",
    "-Wredundant-move",
    "-Wunused-parameter",
    # Colored output
    "-fdiagnostics-color=always",
    # Unrecognized
    # '-Walloc-size',
]

# Add to conly code
CONLY_OPTS = [
    "-Wabsolute-value",
    "-Wmissing-parameter-type",
    "-Wold-style-declaration",
    "-Woverride-init",
]

CXX_OPTS = [
    "-Wsized-deallocation",
    "-Wdeprecated-copy",
    # If changing, likely want to update .bazelrc
    # See https://en.cppreference.com/w/cpp/23
    "-std=c++23",
]

# NOTE: Maybe we should add linkopt too?

def cc_binary(**kwargs):
    _cc_binary(copts = COPTS + CXX_OPTS, **kwargs)

def cc_library(**kwargs):
    _cc_library(copts = COPTS + CXX_OPTS, **kwargs)

def cc_test(**kwargs):
    _cc_test(copts = COPTS + CXX_OPTS, **kwargs)

def c_binary(**kwargs):
    _cc_binary(copts = COPTS + CONLY_OPTS, **kwargs)

def c_library(**kwargs):
    _cc_library(copts = COPTS + CONLY_OPTS, **kwargs)
