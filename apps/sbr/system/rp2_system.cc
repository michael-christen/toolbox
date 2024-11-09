#include "apps/sbr/system/system.h"
#include "hardware/adc.h"
#include "hardware/exception.h"
#include "pico/stdlib.h"
#include "pw_channel/rp2_stdio_channel.h"
#include "pw_cpu_exception/entry.h"
#include "pw_i2c_rp2040/initiator.h"
#include "pw_multibuf/simple_allocator.h"
#include "pw_system/system.h"

#if defined(PICO_RP2040) && PICO_RP2040
#include "system_RP2040.h"
#endif  // defined(PICO_RP2040) && PICO_RP2040
#if defined(PICO_RP2350) && PICO_RP2350
#include "system_RP2350.h"
#endif  // defined(PICO_RP2350) && PICO_RP2350

namespace {

pw::i2c::Initiator& I2cInitiator() {
  constexpr unsigned int kPinSda = 4;
  constexpr unsigned int kPinScl = 5;

  static constexpr pw::i2c::Rp2040Initiator::Config kI2c0Config{
      .clock_frequency = 400'000,
      .sda_pin = kPinSda,
      .scl_pin = kPinScl,
  };

  static pw::i2c::Initiator& i2c0_bus = []() -> pw::i2c::Initiator& {
    static pw::i2c::Rp2040Initiator bus(kI2c0Config, i2c0);
    bus.Enable();
    return bus;
  }();

  return i2c0_bus;
}

}  // namespace

// XXX: Decide on namespace style
namespace apps::sbr::system {

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
  // XXX: Share with lis3mdl
  constexpr pw::i2c::Address kAddress =
      pw::i2c::Address::SevenBit<0b001'1110>();

  static pw::i2c::RegisterDevice reg_device(
      I2cInitiator(), kAddress, cpp20::endian::little,
      pw::i2c::RegisterAddressSize::k1Byte);
  return reg_device;
}

}  // namespace apps::sbr::system
