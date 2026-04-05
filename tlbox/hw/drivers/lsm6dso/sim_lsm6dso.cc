#include "tlbox/hw/drivers/lsm6dso/sim_lsm6dso.h"

namespace hw_drivers {
namespace lsm6dso {


pw::Status SimLsm6dso::DoWriteReadFor(pw::i2c::Address device_address,
                          pw::ConstByteSpan tx_buffer, pw::ByteSpan rx_buffer,
                          pw::chrono::SystemClock::duration timeout,
                          pw::chrono::SystemClock::time_point current_time
                          ) {
  (void) device_address;
  // TODO:
  // - Understand write/then read behavior for register mapping
  if (tx_buffer.size() <= 0) {
    // We mut have a sub-address
    i2c_error_counter_ ++;
    return;
  }
  if (tx_buffer.size() > 1 && rx_buffer.size() > 0) {
    // We don't allow simultaneous reading and writing for this device.
    i2c_error_counter_ ++;
    return;
  }
  std::byte sub_address = tx_buffer[0];
  // XXX: Get offset of a field?
  // XXX: How to interpret a smaller section of a struct?
 std::byte func_cfg_access = basic_map_[0x01];
 // XXX: Use actual overlay
 switch (func_cfg_access) {
   case std::byte(0x80):
     break;
   case std::byte(0x80):
     break;
 }
 if (func_cfg_access == std
}

}
}
