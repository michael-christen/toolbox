#include "platforms/host/initiator_host.h"

namespace platforms {
namespace host {

pw::Status HostInitiator::DoWriteReadFor(
    pw::i2c::Address device_address, pw::ConstByteSpan tx_buffer,
    pw::ByteSpan rx_buffer, pw::chrono::SystemClock::duration timeout) {
  (void)device_address;
  (void)tx_buffer;
  (void)rx_buffer;
  (void)timeout;
  // XXX: Actually do something
  return pw::OkStatus();
}

}  // namespace host
}  // namespace platforms
