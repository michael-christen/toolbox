#pragma once

#include "pw_channel/rp2_stdio_channel.h"
#include "pw_multibuf/simple_allocator.h"
#include "pw_system/system.h"

namespace third_party {
namespace pigweed {
namespace system {

// Initialize PICO_SDK
void CommonRp2Init();

#define PW_RP2_SYSTEM_START(channel_buffer_size)                     \
  static std::byte channel_buffer[2048];                             \
  static pw::multibuf::SimpleAllocator multibuf_alloc(               \
      channel_buffer, pw::System().allocator());                     \
  pw::SystemStart(pw::channel::Rp2StdioChannelInit(multibuf_alloc)); \
  PW_UNREACHABLE;

}  // namespace system
}  // namespace pigweed
}  // namespace third_party
