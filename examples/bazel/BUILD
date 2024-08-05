load("@rules_platform//platform_data:defs.bzl", "platform_data")
load(":my_rules.bzl", "foo_binary", "foo_toolchain")
load(":my_rules_test.bzl", "my_rules_test_suite")


foo_binary(name = "bin1", username = "Alice")

sh_binary(
    name = "cat",
    srcs = ["cat.sh"],
    data = [":bin1"],
)

platform_data(
    name = "cat_bin1_pure",
    platform = ":foo_pure_platform",
    target = ":cat",
    # XXX: should use location, but can't add as attribute of platform_data,
    # and args is overriden by platform_data
    args = ["examples/bazel/bin1"],
)

platform_data(
    name = "cat_bin1_evil",
    platform = ":foo_evil_platform",
    target = ":cat",
    # XXX: should use location, but can't add as attribute of platform_data,
    # and args is overriden by platform_data
    args = ["examples/bazel/bin1"],
)

my_rules_test_suite(name = "my_rules_test")

# Convention has these mostly named toolchain_type and distinguised by path,
# maybe we break that convention in this scenario if we have more?
toolchain_type(name = "toolchain_type")


foo_toolchain(
    name = "foo_rude",
    prefix = "rude_guy",
)

foo_toolchain(
    name = "foo_nice",
    prefix = "nice_guy",
)

foo_toolchain(
    name = "foo_defaulted",
    prefix = "default_guy",
)


# XXX: How to pick a default platform?
# XXX: Use select with my platform's constraints
toolchain(
    name = "foo_nice_toolchain",
    # exec_compatible_with = [
    #     ":foo_pure",
    # ],
    target_compatible_with = [
        ":foo_pure",
    ],
    toolchain = ":foo_nice",
    toolchain_type = ":toolchain_type",
)

toolchain(
    name = "foo_rude_toolchain",
    # exec_compatible_with = [
    #     ":foo_evil",
    # ],
    target_compatible_with = [
        ":foo_evil",
    ],
    toolchain = ":foo_rude",
    toolchain_type = ":toolchain_type",
)

# XXX: Do we require a default toolchain?
toolchain(
    name = "foo_default_toolchain",
    toolchain = ":foo_defaulted",
    toolchain_type = ":toolchain_type",
)

constraint_setting(name = "foo_version")

constraint_value(
    name = "foo_pure",
    constraint_setting = ":foo_version",
)

constraint_value(
    name = "foo_evil",
    constraint_setting = ":foo_version",
)

constraint_value(
    name = "foo_default",
    constraint_setting = ":foo_version",
)

platform(
    name = "foo_pure_platform",
    constraint_values = [
        ":foo_pure",
    ],
)

# XXX: Do we need to forward host constraints to allow exec_compatible_with?
platform(
    name = "foo_evil_platform",
    constraint_values = [
        ":foo_evil",
    ],
)
