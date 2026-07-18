load("@bazel_skylib//lib:unittest.bzl", "analysistest", "asserts")
load(":my_rules.bzl", "foo_binary")

def _foo_binary_test_impl(ctx):
    env = analysistest.begin(ctx)

    actions = analysistest.target_actions(env)
    target = analysistest.target_under_test(env)
    for action in actions:
        # Not really checking much
        asserts.equals(env, 1, len(action.outputs.to_list()))
    return analysistest.end(env)

typ_foo_binary_test = analysistest.make(_foo_binary_test_impl)

# expect_failure: verify that foo_binary fails at analysis time when username is empty.
# analysistest.make(expect_failure=True) inverts the pass/fail logic — the test
# passes only if the target under test fails at analysis time with the given message.
def _foo_binary_empty_username_test_impl(ctx):
    env = analysistest.begin(ctx)
    asserts.expect_failure(env, "username must not be empty")
    return analysistest.end(env)

typ_foo_binary_empty_username_test = analysistest.make(
    _foo_binary_empty_username_test_impl,
    expect_failure = True,
)

# Macro to setup the test
def _test_contents():
    # Leave manual so this only gets built as dependency of the test, not :all
    foo_binary(name = "test_foo", username = "Bob", tags = ["manual"])
    typ_foo_binary_test(name = "foo_binary_test", target_under_test = ":test_foo", timeout = "short")

    foo_binary(name = "test_foo_empty_username", username = "", tags = ["manual"])
    typ_foo_binary_empty_username_test(
        name = "foo_binary_empty_username_test",
        target_under_test = ":test_foo_empty_username",
        timeout = "short",
    )

def my_rules_test_suite(name):
    # Need to instantiate
    _test_contents()

    native.test_suite(
        name = name,
        tests = [
            ":foo_binary_test",
            ":foo_binary_empty_username_test",
        ],
    )
