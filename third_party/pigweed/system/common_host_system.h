#pragma once

#include "pw_assert/check.h"
#include "pw_channel/stream_channel.h"
#include "pw_digital_io/digital_io.h"
#include "pw_multibuf/simple_allocator.h"
#include "pw_system/io.h"
#include "pw_system/system.h"
#include "pw_thread_stl/options.h"

namespace third_party {
namespace pigweed {
namespace system {

// Keep internal for use by HOST_SYSTEM_START
namespace internal {

/// Does most of the necessary setup for host start:
/// - configures ctrl-c handling
/// - prints user guides
void CommonHostStartSetup(const char* bazel_console_path);

}  // namespace internal

}  // namespace system
}  // namespace pigweed
}  // namespace third_party

/// Do all of the work necessary to start a host system.
/// - Calls CommonHostStartSetup(ctrl-c + guide)
/// - Constructs an allocator and stream channel, returning the channel
///
/// Users are expected to invoke like this:
///
/// #include "third_party/pigweed/system/common_host_system.h"
///
/// void Start() {
///   // <insert custom code here, etc.>
///
///   PW_HOST_SYSTEM_START(16384, "//apps/<myapp>:simulator_console")
/// }
///
/// This is a macro in order to handle the non-destructible StreamChannel and
/// the PW_UNREACHABLE, note that we implicitly include these dependencies
/// (we may want to re-evaluate whether we should re-import in callers)
#define PW_HOST_SYSTEM_START(channel_buffer_size, bazel_console_path)      \
  ::third_party::pigweed::system::internal::CommonHostStartSetup(          \
      bazel_console_path);                                                 \
  static std::byte channel_buffer[channel_buffer_size];                    \
  static pw::multibuf::SimpleAllocator multibuf_alloc(                     \
      channel_buffer, pw::System().allocator());                           \
  static pw::NoDestructor<pw::channel::StreamChannel> channel(             \
      multibuf_alloc, pw::system::GetReader(), pw::thread::stl::Options(), \
      pw::system::GetWriter(), pw::thread::stl::Options());                \
  pw::SystemStart(channel->channel());                                     \
  PW_UNREACHABLE;
