#include "apps/sbr/system/system.h"
#include "hw_drivers/lis3mdl/lis3mdl.h"
#include "pw_i2c_rp2040/initiator.h"

namespace {

pw::i2c::Initiator& I2cInitiator() {
  constexpr unsigned int kPinSda = 4;
  constexpr unsigned int kPinScl = 5;

  static constexpr pw::i2c::Rp2040Initiator::Config kI2c0Config{
      .clock_frequency_hz = 400'000,
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

#include "third_party/pigweed/system/common_rp2_system.h"

namespace apps {
namespace sbr {
namespace system {

void Init() { third_party::pigweed::system::CommonRp2Init(); }

void Start(){PW_RP2_SYSTEM_START(2048)}

pw::i2c::RegisterDevice& LIS3MDLRegisterDevice() {
  static pw::i2c::RegisterDevice reg_device(
      I2cInitiator(), hw_drivers::lis3mdl::kHighAddress, cpp20::endian::little,
      pw::i2c::RegisterAddressSize::k1Byte);
  return reg_device;
}

}  // namespace system
}  // namespace sbr
}  // namespace apps
