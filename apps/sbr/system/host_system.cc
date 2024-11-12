#include "third_party/pigweed/system/common_host_system.h"
#include "platforms/host/initiator_host.h"
#include "pw_i2c/address.h"

#include "apps/sbr/system/system.h"

namespace apps {
namespace sbr {
namespace system {

void Init() {}

void Start() {
  // third_party::pigweed::system::
  PW_HOST_SYSTEM_START(16384, "//apps/sbr:simulator_console")
}

pw::i2c::RegisterDevice& LIS3MDLRegisterDevice() {
  constexpr pw::i2c::Address kAddress = pw::i2c::Address::SevenBit<0x01>();

  static platforms::host::HostInitiator initiator;
  static pw::i2c::RegisterDevice reg_device(
      initiator, kAddress, cpp20::endian::little,
      pw::i2c::RegisterAddressSize::k1Byte);
  return reg_device;
}

}  // namespace system
}  // namespace sbr
}  // namespace apps
