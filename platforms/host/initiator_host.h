#pragma once

#include "pw_bytes/span.h"
#include "pw_i2c/initiator.h"
#include "pw_i2c/address.h"

namespace platforms {
namespace host {

class HostInitiator : public pw::i2c::Initiator {
 public:
  explicit constexpr HostInitiator() {}

 private:
  // Implements a mocked backend for the i2c initiator.
  //
  // Expects (via Gtest):
  // tx_buffer == expected_transaction_tx_buffer
  // tx_buffer.size() == expected_transaction_tx_buffer.size()
  // rx_buffer.size() == expected_transaction_rx_buffer.size()
  //
  // Asserts:
  // When the number of calls to this method exceed the number of expected
  //    transactions.
  //
  // Returns:
  // Specified transaction return type
  pw::Status DoWriteReadFor(pw::i2c::Address device_address,
                            pw::ConstByteSpan tx_buffer,
                            pw::ByteSpan rx_buffer,
                            pw::chrono::SystemClock::duration timeout) override;

};

}
}
