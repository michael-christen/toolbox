# C++ Testing

Two build rules are used for C++ tests, depending on whether Pigweed integration
is required.

## `cc_test` — host unit tests

Use `cc_test` (from `//bzl:cc.bzl`) for tests that run purely on the host with
no Pigweed backends. Gazelle auto-generates the BUILD target and wires in
`//tlbox/testing:gtest_main`.

```cpp
#include <gtest/gtest.h>

TEST(MyTest, BasicBehaviour) {
    EXPECT_EQ(1 + 1, 2);
}
```

**References:**

- [Google Test Primer](https://google.github.io/googletest/primer.html)
- [Google Test Advanced Topics](https://google.github.io/googletest/advanced.html)
  (fixtures, parametrized tests, death tests)

## `pw_cc_test` — Pigweed-integrated tests

Use `pw_cc_test` (from `//bzl:cc.bzl`) for tests that need Pigweed backends —
I2C mocks, async dispatchers, allocator testing, etc. These use the same Google
Test API (`TEST`, `EXPECT_*`, `ASSERT_*`) as `cc_test`.

```cpp
#include "pw_unit_test/framework.h"

TEST(MyPwTest, BasicBehaviour) {
    EXPECT_EQ(1 + 1, 2);
}
```

**References:**

- [pw_unit_test documentation](https://pigweed.dev/pw_unit_test/)

## Why two rules?

`pw_cc_test` pulls in Pigweed's build system integration: facade backends,
linker scripts, and the `pw_unit_test` framework. `cc_test` doesn't need any of
that for pure host tests. The test _syntax_ is identical (both use the Google
Test API); only the build rule differs.

## `PW_LOG_*` in `pw_cc_test`

`PW_LOG_INFO`, `PW_LOG_DEBUG`, etc. are visible in `pw_cc_test` output. The log
backend chain is:

```
pw_log → pw_log_string → //tlbox/testing:log_string_handler → pw_sys_io (stdio)
```

`//tlbox/testing:log_string_handler` is a minimal handler that writes directly
to `pw_sys_io` (configured as stdio on host). The default Pigweed handler
(`pw_system:log_backend`) routes messages into a MultiSink ring buffer drained
by the RPC stack; draining that buffer in tests would require full `pw_system`
initialization (RTOS threads, socket I/O), which is impractical for unit tests.

Optionally set a module name for cleaner output:

```cpp
#define PW_LOG_MODULE_NAME "MY_MODULE"
#include "pw_log/log.h"

TEST(MyTest, Foo) {
    PW_LOG_INFO("value: %d", 42);  // prints: [MY_MODULE] value: 42
}
```
