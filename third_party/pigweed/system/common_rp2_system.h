#pragma once

#include "pw_channel/rp2_stdio_channel.h"
#include "pw_multibuf/simple_allocator.h"
#include "pw_system/system.h"

namespace third_party {
namespace pigweed {
namespace system {

// Initialize PICO_SDK
void CommonRp2Init();

// This is a macro that sets up a channel of specified size, an allocator, and
// then starts the system.
//
// Example Usage:
//
/// #include "third_party/pigweed/system/common_rp2_system.h"
///
/// void Start() {
///   // <insert custom code here, etc.>
///
///   PW_RP2_SYSTEM_START(2048)
/// }
#define PW_RP2_SYSTEM_START(channel_buffer_size)                         \
  static std::byte channel_buffer[channel_buffer_size];                  \
  static pw::multibuf::SimpleAllocator multibuf_alloc(                   \
      channel_buffer, pw::System().allocator());                         \
  pw::SystemStart(                                                       \
      pw::channel::Rp2StdioChannelInit(multibuf_alloc, multibuf_alloc)); \
  PW_UNREACHABLE;

}  // namespace system
}  // namespace pigweed
}  // namespace third_party
