#include "tlbox/hw/drivers/lsm6dso/sim_lsm6dso.h"

namespace hw_drivers {
namespace lsm6dso {

pw::Status SimLsm6dso::DoWriteReadFor(
    pw::i2c::Address device_address, pw::ConstByteSpan tx_buffer,
    pw::ByteSpan rx_buffer, pw::chrono::SystemClock::duration timeout,
    pw::chrono::SystemClock::time_point current_time) {
  // TODO: Implement register map simulation.
  // - Handle write (sub-address) then read behavior
  // - Route to correct register bank based on FUNC_CFG_ACCESS bits
  (void)device_address;
  (void)tx_buffer;
  (void)rx_buffer;
  (void)timeout;
  (void)current_time;
  return pw::Status::Unimplemented();
}

}  // namespace lsm6dso
}  // namespace hw_drivers
