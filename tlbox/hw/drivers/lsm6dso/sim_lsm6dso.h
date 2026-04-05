#pragma once

#include <array>
#include <cstdint>

#include "pw_bytes/span.h"
#include "pw_i2c/address.h"
#include "pw_i2c/initiator.h"
#include "pw_status/status.h"

namespace hw_drivers {
namespace lsm6dso {

class SimLsm6dso : public pw::i2c::Initiator {
 public:
  pw::Status DoWriteReadFor(
      pw::i2c::Address device_address, pw::ConstByteSpan tx_buffer,
      pw::ByteSpan rx_buffer, pw::chrono::SystemClock::duration timeout,
      pw::chrono::SystemClock::time_point current_time) override;

 private:
  std::array<std::byte, 0x7E + 1> basic_map_{};
  std::array<std::byte, 0x67 + 1> embedded_function_map_{};
  std::array<std::byte, 0xD5 + 1> embedded_advanced_function_map_{};
  std::array<std::byte, 0x22 + 1> sensor_hub_map_{};

  uint32_t i2c_error_counter_ = 0;
};

}  // namespace lsm6dso
}  // namespace hw_drivers
