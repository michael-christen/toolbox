load("@rules_platform//platform_data:defs.bzl", "platform_data")
load(":my_rules.bzl", "foo_binary", "foo_toolchain")
load(":my_rules_test.bzl", "my_rules_test_suite")

package(default_visibility = ["//visibility:private"])

filegroup(
    name = "python_source",
    srcs = glob(["*.py"], allow_empty=True) + [
    ],
    visibility = ["//visibility:public"],
)

my_rules_test_suite(name = "my_rules_test")

# Define constraints to select our toolchain

# Select a default, otherwise we'll need a default toolchain
constraint_setting(
    name = "foo_version",
    default_constraint_value = ":foo_pure",
)

constraint_value(
    name = "foo_pure",
    constraint_setting = ":foo_version",
)

constraint_value(
    name = "foo_evil",
    constraint_setting = ":foo_version",
)

# Specify platforms that declare a list of chosen constraints

platform(
    name = "foo_pure_platform",
    constraint_values = [
        ":foo_pure",
    ],
)

platform(
    name = "foo_evil_platform",
    constraint_values = [
        ":foo_evil",
    ],
)

# Instantiate foo_toolchains that select FooInfo (prefix)

foo_toolchain(
    name = "foo_rude",
    prefix = "rude_guy",
)

foo_toolchain(
    name = "foo_nice",
    prefix = "nice_guy",
)

# Specify an instance of toolchain_type, so that we can associate this with the
# foo_toolchain instances above
# Convention has these mostly named toolchain_type and distinguised by path,
# maybe we break that convention in this scenario if we have more?
toolchain_type(name = "toolchain_type")

# Bind foo_toolchain to toolchain_type based on constraints

# No need to specify exec_compatible_with as we expect to run on host anyways
toolchain(
    name = "foo_nice_toolchain",
    target_compatible_with = [
        ":foo_pure",
    ],
    toolchain = ":foo_nice",
    toolchain_type = ":toolchain_type",
)

toolchain(
    name = "foo_rude_toolchain",
    target_compatible_with = [
        ":foo_evil",
    ],
    toolchain = ":foo_rude",
    toolchain_type = ":toolchain_type",
)

# Define our products

foo_binary(
    name = "bin1",
    # Here's an example of using select with my platform's constraints
    username = select({
        ":foo_pure": "Alice",
        ":foo_evil": "Bob",
    }),
)

sh_binary(
    name = "cat",
    srcs = ["cat.sh"],
    data = [":bin1"],
)

# Overwrite platform for the executable and dependents to enable multi-platform
# builds with a single invocation

platform_data(
    name = "cat_bin1_pure",
    # NOTE: should use location, but can't add as attribute of platform_data,
    # and args is overriden by platform_data
    args = ["examples/bazel/bin1"],
    platform = ":foo_pure_platform",
    target = ":cat",
)

platform_data(
    name = "cat_bin1_evil",
    # NOTE: should use location, but can't add as attribute of platform_data,
    # and args is overriden by platform_data
    args = ["examples/bazel/bin1"],
    platform = ":foo_evil_platform",
    target = ":cat",
)

# Prove this is working as expected (changing prefix)
sh_test(
    name = "cat_bin1_pure_test",
    srcs = ["check_equality.sh"],
    args = [
        "$(location :cat_bin1_pure)",
        "'Hello from nice_guy to Alice!'",
    ],
    data = [":cat_bin1_pure"],
)

sh_test(
    name = "cat_bin1_evil_test",
    srcs = ["check_equality.sh"],
    args = [
        "$(location :cat_bin1_evil)",
        "'Hello from rude_guy to Bob!'",
    ],
    data = [":cat_bin1_evil"],
)
