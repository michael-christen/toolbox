// pw_log_string handler backend for use in pw_cc_test targets.
//
// pw_system:log_backend (the default handler) routes messages into a MultiSink
// ring buffer drained by the RPC stack. That stack never starts in tests, so
// PW_LOG_* calls are silently dropped. This handler writes directly to
// pw_sys_io (configured as stdio on host), making PW_LOG visible in test
// output without requiring full pw_system initialisation.

#include <stdarg.h>

#include "pw_string/string_builder.h"
#include "pw_sys_io/sys_io.h"

// Implements the pw_log_string handler C ABI without including
// pw_log_string/handler.h to avoid a circular facade dependency.
extern "C" void pw_log_string_HandleMessageVaList(
    int /*level*/, unsigned int /*flags*/, const char* module_name,
    const char* /*file_name*/, int /*line_number*/, const char* message,
    va_list args) {
  // 256 bytes covers typical log lines; longer messages are silently truncated.
  pw::StringBuffer<256> sb;
  sb.Format("[%s] ", module_name);
  sb.FormatVaList(message, args);
  pw::sys_io::WriteLine(sb.c_str()).IgnoreError();
}
