#include <chrono>
#include <cstdint>
#include <iostream>
#include <vector>

#include "hw_drivers/lis3mdl/lis3mdl.emb.h"
#include "hw_drivers/lis3mdl/lis3mdl.h"
#include "hw_drivers/lis3mdl/lis3mdl.pb.h"
#include "pw_bytes/array.h"
#include "pw_bytes/bit.h"
#include "pw_i2c/address.h"
#include "pw_i2c/initiator_mock.h"
#include "pw_i2c/register_device.h"
#include "pw_log/log.h"
#include "pw_result/result.h"
#include "pw_unit_test/framework.h"

namespace hw_drivers {
namespace lis3mdl {

namespace {
using namespace std::chrono_literals;

constexpr auto kI2cTimeout = 100ms;

// TODO(#147): How to prevent bifurcation of pw_cc_test and cc_test?
TEST(I2CTestSuite, I2CTransactions) {
  constexpr pw::i2c::Address kAddress = pw::i2c::Address::SevenBit<0x01>();
  constexpr auto kExpectedWrite = pw::bytes::Array<1, 2, 3, 4, 5, 6>();
  constexpr auto kJustReg = pw::bytes::Array<1>();
  constexpr auto kMockRead =
      pw::bytes::Array<1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12>();
  constexpr auto kControlWrite =
      pw::bytes::Array<static_cast<uint8_t>(RegisterAddress::CONTROL),  // 0x20
                       0xFC,  // 0b1111'1100,
                       0x00, 0x00, 0x0C, 0x40>();
  constexpr auto kDataRead = pw::bytes::Array<0, 0, 0, 0, 0, 0, 0, 0, 0>();
  constexpr auto kDataReg =
      pw::bytes::Array<static_cast<uint8_t>(RegisterAddress::DATA)>();
  auto expected_transactions = pw::i2c::MakeExpectedTransactionArray({
      pw::i2c::WriteTransaction(pw::OkStatus(), kAddress, kExpectedWrite,
                                kI2cTimeout),
      pw::i2c::Transaction(pw::OkStatus(), kAddress, kJustReg, kMockRead,
                           kI2cTimeout),
      pw::i2c::WriteTransaction(pw::OkStatus(), kAddress, kControlWrite,
                                kI2cTimeout),
      pw::i2c::Transaction(pw::OkStatus(), kAddress, kDataReg, kDataRead,
                           kI2cTimeout),
  });
  pw::i2c::MockInitiator initiator(expected_transactions);
  pw::i2c::RegisterDevice reg_device(initiator, kAddress, cpp20::endian::little,
                                     pw::i2c::RegisterAddressSize::k1Byte);
  constexpr auto kRegWrite = pw::bytes::Array<2, 3, 4, 5, 6>();  // XXX: dangling-gsl
  std::array<std::byte, 12> raw_buf = {std::byte{0}};
  auto buf = pw::as_writable_bytes(pw::span(raw_buf));
  auto status = reg_device.WriteRegisters(
      kAddress.GetSevenBit() /*register_address*/, kRegWrite, buf, kI2cTimeout);
  // pw::ConstByteSpan kActualWrite = pw::bytes::Array<1, 2, 3>();
  // pw::Status status = initiator.WriteFor(kAddress, kActualWrite,
  // kI2cTimeout);
  EXPECT_EQ(status, pw::OkStatus());
  status = reg_device.ReadRegisters(kAddress.GetSevenBit(), buf, kI2cTimeout);
  EXPECT_EQ(status, pw::OkStatus());
  EXPECT_EQ(raw_buf, kMockRead);

  LIS3MDLControl control;
  const ::hw_drivers_lis3mdl_LIS3MDLConfiguration configuration{
      .has_temperature_enabled = true,
      // Temperature
      .temperature_enabled = true,
      .has_allowable_rms_noise_ug = true,
      .allowable_rms_noise_ug = 3'500,
      .has_data_rate_millihz = true,
      .data_rate_millihz = 80'000,
      .has_scale_gauss = true,
      .scale_gauss = 4,
  };

  auto result = SolveConfiguration(configuration, &control);
  EXPECT_TRUE(std::holds_alternative<::hw_drivers_lis3mdl_LIS3MDLConfiguration>(result));

  // COULD: Make this a utility?
  pw::StringBuffer<sizeof(control.bytes.data()) * 3 + 3> sb;
  sb << "0x ";
  for (const auto c : control.bytes) {
    sb << std::format("{:02X} ", static_cast<uint8_t>(c));
  }
  std::cout << "Control Bytes: " << sb.c_str() << std::endl;
  // TODO(#147): How to show LOG in test?
  PW_LOG_INFO("Control bytes: %s", sb.c_str());

  status = ApplyControlToDevice(control, &reg_device);
  EXPECT_EQ(status, pw::OkStatus());

  LIS3MDLData data;
  status = ReadFromDevice(&data, &reg_device);
  EXPECT_EQ(status, pw::OkStatus());

  // NOTE: This is a fairly annoying check, it doesn't say what's wrong
  EXPECT_EQ(initiator.Finalize(), pw::OkStatus());
}

}  // namespace

}  // namespace lis3mdl
}  // namespace hw_drivers
