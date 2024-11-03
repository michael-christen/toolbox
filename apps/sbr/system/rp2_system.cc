#include "apps/sbr/system/system.h"

#include "pw_channel/rp2_stdio_channel.h"
#include "pw_cpu_exception/entry.h"
#include "pw_multibuf/simple_allocator.h"
#include "pw_system/system.h"

#include "hardware/adc.h"
#include "hardware/exception.h"
#include "pico/stdlib.h"

#if defined(PICO_RP2040) && PICO_RP2040
#include "system_RP2040.h"
#endif  // defined(PICO_RP2040) && PICO_RP2040
#if defined(PICO_RP2350) && PICO_RP2350
#include "system_RP2350.h"
#endif  // defined(PICO_RP2350) && PICO_RP2350

#include "platforms/host/initiator_host.h"

void Init() {
  // PICO_SDK inits.
  SystemInit();
  stdio_init_all();
  setup_default_uart();
  stdio_usb_init();
  adc_init();

  // Install the CPU exception handler.
  exception_set_exclusive_handler(HARDFAULT_EXCEPTION, pw_cpu_exception_Entry);
}

void Start() {
  static std::byte channel_buffer[2048];
  static pw::multibuf::SimpleAllocator multibuf_alloc(channel_buffer,
                                                      pw::System().allocator());
  pw::SystemStart(pw::channel::Rp2StdioChannelInit(multibuf_alloc));
  PW_UNREACHABLE;
}

// XXX: Better
pw::i2c::RegisterDevice& LIS3MDLRegisterDevice() {
  constexpr pw::i2c::Address kAddress = pw::i2c::Address::SevenBit<0x01>();

  static platforms::host::HostInitiator initiator;
  static pw::i2c::RegisterDevice reg_device(initiator, kAddress, cpp20::endian::little,
      pw::i2c::RegisterAddressSize::k1Byte);
  return reg_device;
}
