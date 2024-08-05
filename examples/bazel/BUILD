load(":my_rules.bzl", "foo_binary", "foo_toolchain")
load(":my_rules_test.bzl", "my_rules_test_suite")


foo_binary(name = "bin1", username = "Alice")

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


toolchain(
    name = "foo_nice_toolchain",
    # exec_compatible_with, target_compatible_with
    toolchain = ":foo_nice",
    toolchain_type = ":toolchain_type",
)

toolchain(
    name = "foo_rude_toolchain",
    # exec_compatible_with, target_compatible_with
    toolchain = ":foo_rude",
    toolchain_type = ":toolchain_type",
)
