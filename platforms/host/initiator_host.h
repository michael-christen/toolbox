#pragma once

#include "pw_bytes/span.h"
#include "pw_i2c/address.h"
#include "pw_i2c/initiator.h"

namespace platforms {
namespace host {

class HostInitiator : public pw::i2c::Initiator {
 public:
  explicit constexpr HostInitiator() {}

 private:
  // Implements a mocked backend for the i2c initiator.
  //
  // Simply does a no-op and returns OkStatus
  pw::Status DoWriteReadFor(pw::i2c::Address device_address,
                            pw::ConstByteSpan tx_buffer, pw::ByteSpan rx_buffer,
                            pw::chrono::SystemClock::duration timeout) override;
};

}  // namespace host
}  // namespace platforms
