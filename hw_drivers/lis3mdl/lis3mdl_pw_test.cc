#include "hw_drivers/lis3mdl/lis3mdl.h"

#include <chrono>
#include <cstdint>
#include <vector>

#include "pw_bytes/bit.h"
#include "pw_bytes/array.h"
#include "pw_i2c/address.h"
#include "pw_i2c/initiator_mock.h"
#include "pw_i2c/register_device.h"
#include "pw_result/result.h"
#include "pw_unit_test/framework.h"
#include "pw_log/log.h"

#include "hw_drivers/lis3mdl/lis3mdl.emb.h"
#include "hw_drivers/lis3mdl/lis3mdl.pb.h"


using namespace std::chrono_literals;

namespace hw_drivers {
namespace lis3mdl {

namespace {

// XXX: How to prevent bifurcation of pw_cc_test and cc_test?
TEST(I2CTestSuite, I2CTransactions) {
  constexpr pw::i2c::Address kAddress = pw::i2c::Address::SevenBit<0x01>();
  constexpr auto kExpectedWrite = pw::bytes::Array<1, 2, 3, 4, 5, 6>();
  constexpr auto kJustReg = pw::bytes::Array<1>();
  constexpr auto kMockRead = pw::bytes::Array<1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12>();
  constexpr auto kControlWrite = pw::bytes::Array<
    static_cast<uint8_t>(RegisterAddress::CONTROL),  // 0x20
    0xFC,  // 0b1111'1100,
    0x00,
    0x00,
    0x0C,
    0x00
  >();
  auto expected_transactions = pw::i2c::MakeExpectedTransactionArray(
    {
      pw::i2c::WriteTransaction(pw::OkStatus(), kAddress, kExpectedWrite, 1ms),
      pw::i2c::Transaction(pw::OkStatus(), kAddress, kJustReg, kMockRead, 1ms),
      pw::i2c::WriteTransaction(pw::OkStatus(), kAddress, kControlWrite, 1ms),
    }
  );
  pw::i2c::MockInitiator initiator(expected_transactions);
  pw::i2c::RegisterDevice reg_device(initiator, kAddress, cpp20::endian::little,
                                     pw::i2c::RegisterAddressSize::k1Byte);
  pw::ConstByteSpan kRegWrite = pw::bytes::Array<2, 3, 4, 5, 6>();
  std::array<std::byte, 12> raw_buf = {std::byte{0}};
  auto buf = pw::as_writable_bytes(pw::span(raw_buf));
  auto status = reg_device.WriteRegisters(
      kAddress.GetSevenBit() /*register_address*/, kRegWrite, buf, 1ms);
  // pw::ConstByteSpan kActualWrite = pw::bytes::Array<1, 2, 3>();
  // pw::Status status = initiator.WriteFor(kAddress, kActualWrite, 1ms);
  EXPECT_EQ(status, pw::OkStatus());
  status = reg_device.ReadRegisters(
      kAddress.GetSevenBit(),
      buf,
      1ms
  );
  EXPECT_EQ(status, pw::OkStatus());
  EXPECT_EQ(raw_buf, kMockRead);

  // XXX: new section?
  LIS3MDLControl control;
  LIS3MDLConfiguration configuration;
  configuration.set_temperature_enabled(true);
  configuration.set_allowable_rms_noise_ug(3'500);
  configuration.set_data_rate_millihz(80'000);
  configuration.set_scale_gauss(4);

  auto result = SolveConfiguration(configuration, &control);
  EXPECT_TRUE(result.has_value());
  auto actual_config = result.value();

  // Ensuring we are configuring exactly as desired
  // XXX: EXPECT_EQ(result.value(), configuration);
  // XXX: Do I need + 1?
  pw::StringBuffer<sizeof(control.bytes.data()) * 2 + 2> sb;
  sb << "0x";
  // XXX: Maybe should show as opposite?
  for (const auto c : control.bytes) {
    sb << std::format("{:#x}", static_cast<uint8_t>(c));
  }
  std::cout << "Control Bytes: " << sb.c_str() << std::endl;
  // XXX: How to show LOG in test?
  PW_LOG_INFO("Control bytes: %s", sb.c_str());

  status = ApplyControlToDevice(control, &reg_device);
  EXPECT_EQ(status, pw::OkStatus());

  // XXX: This is a fairly annoying check, it doesn't say what's wrong
  EXPECT_EQ(initiator.Finalize(), pw::OkStatus());
}

}

}
}
