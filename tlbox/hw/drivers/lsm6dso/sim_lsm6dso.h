#pragma once

#include "pw_bytes/span.h"
#include "pw_i2c/address.h"
#include "pw_i2c/initiator.h"
#include "pw_status/status.h"

namespace hw_drivers {
namespace lsm6dso {

// Simulated LSM6DSO i2c initiator for host-side testing.
// TODO(#302): Implement register map simulation.
class SimLsm6dso : public pw::i2c::Initiator {
 public:
  pw::Status DoWriteReadFor(pw::i2c::Address device_address,
                            pw::ConstByteSpan tx_buffer, pw::ByteSpan rx_buffer,
                            pw::chrono::SystemClock::duration timeout) override;
};

}  // namespace lsm6dso
}  // namespace hw_drivers
