# Bazel Example

This directory is a place for me to learn about bazel specifics, test out new
ideas, and hopefully leave a few good examples of how to do certain bazel
things.

Most of this is coming from bazel's documentation and copious examples:

- [Tutorials](https://bazel.build/rules/rules-tutorial)
- [Examples](https://github.com/bazelbuild/examples/tree/master/rules)
- [Reference](https://bazel.build/reference/be/general#config_setting)
- https://bazel.build/docs/configurable-attributes
- Globals: https://bazel.build/versions/6.3.0/rules/lib/globals &
  https://bazel.build/rules/lib/globals

## Description

- [my_rules.bzl](./my_rules.bzl)
  - an example rule
- [my_rules_test.bzl](./my_rules_test.bzl)
  - a test for `my_rules.bzl`
- [BUILD](./BUILD)
  - instantiate the rule and test

## More to Do

- [ ] Aspect usage
- [ ] genrule

## Questions

- what is the difference between config_setting/value and
  constraint_setting/value
  - there isn't config_value? just config_setting, which describes kinda
    arbitrary info?
  - constraints are essentially enums used by platforms
