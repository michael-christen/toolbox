# C++ Testing

`cc_test` (from `//bzl:cc.bzl`) is the single rule for all C++ tests. It
auto-selects the right underlying framework based on your includes:

- **`#include "pw_unit_test/framework.h"`** → delegates to `pw_cc_test`, pulling
  in Pigweed build-system integration (facade backends, I2C mocks, async
  dispatchers, etc.)
- **`#include <gtest/gtest.h>`** → standard `cc_test` with shared copts

The test syntax is identical in both cases (Google Test API: `TEST`, `EXPECT_*`,
`ASSERT_*`). Gazelle generates the BUILD target automatically.

## Host-only tests

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

## Pigweed-integrated tests

Include `pw_unit_test/framework.h` to opt in to Pigweed integration (gazelle
adds `@pigweed//pw_unit_test` to deps automatically):

```cpp
#include "pw_unit_test/framework.h"

TEST(MyPwTest, BasicBehaviour) {
    EXPECT_EQ(1 + 1, 2);
}
```

**References:**

- [pw_unit_test documentation](https://pigweed.dev/pw_unit_test/)

## `PW_LOG_*` in Pigweed tests

`PW_LOG_INFO`, `PW_LOG_DEBUG`, etc. are visible in test output. The log backend
chain is:

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
