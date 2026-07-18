#include <chrono>
#include <cstdint>
#include <vector>

#include "pw_bytes/array.h"
#include "pw_bytes/bit.h"
#include "pw_i2c/address.h"
#include "pw_i2c/initiator_mock.h"
#include "pw_i2c/register_device.h"
#include "pw_log/log.h"
#include "pw_result/result.h"
#include "pw_unit_test/framework.h"
#include "tlbox/hw/drivers/lis3mdl/lis3mdl.emb.h"
#include "tlbox/hw/drivers/lis3mdl/lis3mdl.h"
#include "tlbox/hw/drivers/lis3mdl/lis3mdl.pb.h"

namespace hw_drivers {
namespace lis3mdl {

namespace {

// Pure computation tests (no I2C) ----------------------------------------

TEST(Lis3mdlTest, Offset) {
  uint8_t buf[Offset::MaxSizeInBytes()];

  auto offset_view = MakeOffsetView(buf, std::size(buf));
  offset_view.out_x().Write(0x1234);

  EXPECT_EQ(offset_view.out_x().Read(), 0x1234);
  EXPECT_EQ(buf[0], 0x34);
  EXPECT_EQ(buf[1], 0x12);
}

TEST(Lis3mdlTest, EmbossAndCalculationsAreCorrect) {
  uint8_t buf[Control::MaxSizeInBytes()];

  auto control_view = MakeControlView(buf, std::size(buf));
  control_view.temperature_enable().Write(true);

  EXPECT_TRUE(control_view.temperature_enable().Read());
  EXPECT_TRUE(buf[0] & 0x80);
}

TEST(Lis3mdlTest, SolveConfigurationInvalidConfig) {
  ::hw_drivers_lis3mdl_LIS3MDLConfiguration configuration;
  LIS3MDLControl control;
  auto control_view =
      MakeControlView(control.bytes.data(), std::size(control.bytes));
  auto result = SolveConfiguration(configuration, &control);
  ASSERT_TRUE(std::holds_alternative<ConfigurationError>(result));
  EXPECT_EQ(std::get<ConfigurationError>(result),
            ConfigurationError::kInvalidConfig);

  configuration = ::hw_drivers_lis3mdl_LIS3MDLConfiguration{
      .has_temperature_enabled = true,
      // Temperature
      .temperature_enabled = false,
      .has_allowable_rms_noise_ug = true,
      .allowable_rms_noise_ug = 3'500,
      .has_data_rate_millihz = true,
      .data_rate_millihz = 80'000,
      .has_scale_gauss = true,
      .scale_gauss = 4,
  };

  result = SolveConfiguration(configuration, &control);
  ASSERT_TRUE(std::holds_alternative<::hw_drivers_lis3mdl_LIS3MDLConfiguration>(
      result));
  auto actual_config =
      std::get<::hw_drivers_lis3mdl_LIS3MDLConfiguration>(result);
  ASSERT_TRUE(actual_config.has_temperature_enabled);
  EXPECT_FALSE(actual_config.temperature_enabled);
  EXPECT_FALSE(control_view.temperature_enable().Read());

  // Test Plan:
  // - rms noise coverage
  // - check math on frequency decision / can I break it?
}

TEST(Lis3mdlTest, ReadData) {
  LIS3MDLData d;
  auto view = MakeDataView(d.bytes.data(), std::size(d.bytes));
  static_assert(Data::MaxSizeInBytes() == 9);
  static_assert(Data::IntrinsicSizeInBytes() == 9);
  EXPECT_EQ(d.bytes.size(), 9u);
  EXPECT_EQ(std::size(d.bytes), 9u);
  // TODO(#144): Why aren't these equal / why is sizeof d.bytes.data() 8?
  // EXPECT_EQ(sizeof(d.bytes.data()), 9u);
  // EXPECT_EQ(sizeof(d.bytes.data()), d.bytes.size());

  // Check that reading uninitialized doesn't crash
  auto reading = InterpretReading(kFullScale4LSBPerGauss, d);

  // Check simple available / overrun behavior
  view.zyxd_available().Write(1);
  view.zyx_overrun().Write(1);
  reading = InterpretReading(kFullScale4LSBPerGauss, d);
  EXPECT_TRUE(reading.data_fresh);
  EXPECT_TRUE(reading.data_overrun);

  view.zyx_overrun().Write(0);
  reading = InterpretReading(kFullScale4LSBPerGauss, d);
  EXPECT_TRUE(reading.data_fresh);
  EXPECT_FALSE(reading.data_overrun);

  view.zyxd_available().Write(0);
  reading = InterpretReading(kFullScale4LSBPerGauss, d);
  EXPECT_FALSE(reading.data_fresh);
  EXPECT_FALSE(reading.data_overrun);

  // Check Temperature
  view.temperature_out().Write(0);
  reading = InterpretReading(kFullScale4LSBPerGauss, d);
  EXPECT_EQ(reading.temperature_dc, 250);

  view.out_x().Write(-100);
  view.out_y().Write(0);
  view.out_z().Write(200);
  reading = InterpretReading(kFullScale4LSBPerGauss, d);
  EXPECT_EQ(reading.magnetic_strength_x_ug, -14'615);
  EXPECT_EQ(reading.magnetic_strength_y_ug, 0);
  EXPECT_EQ(reading.magnetic_strength_z_ug, 29'231);

  // Changing scale changes the behavior (eye-balled around 4x)
  reading = InterpretReading(kFullScale16LSBPerGauss, d);
  EXPECT_EQ(reading.magnetic_strength_x_ug, -58'445);
  EXPECT_EQ(reading.magnetic_strength_y_ug, 0);
  EXPECT_EQ(reading.magnetic_strength_z_ug, 116'890);
}

// I2C integration tests --------------------------------------------------

TEST(Lis3mdlTest, I2CTransactions) {
  using namespace std::chrono_literals;
  constexpr auto kI2cTimeout = 100ms;
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
  constexpr auto kRegWrite = pw::bytes::Array<2, 3, 4, 5, 6>();
  std::array<std::byte, 12> raw_buf = {std::byte{0}};
  auto buf = pw::as_writable_bytes(pw::span(raw_buf));
  auto status = reg_device.WriteRegisters(
      kAddress.GetSevenBit() /*register_address*/, kRegWrite, buf, kI2cTimeout);
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
  EXPECT_TRUE(std::holds_alternative<::hw_drivers_lis3mdl_LIS3MDLConfiguration>(
      result));

  // COULD: Make this a utility?
  pw::StringBuffer<sizeof(control.bytes.data()) * 3 + 3> sb;
  sb << "0x ";
  for (const auto c : control.bytes) {
    sb << std::format("{:02X} ", static_cast<uint8_t>(c));
  }
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
