#include "tlbox/hw/drivers/lis3mdl/lis3mdl.h"

#include <gtest/gtest.h>

#include <cstdint>
#include <vector>

#include "tlbox/hw/drivers/lis3mdl/lis3mdl.emb.h"
#include "tlbox/hw/drivers/lis3mdl/lis3mdl.pb.h"

namespace hw_drivers {
namespace lis3mdl {

namespace {

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

}  // namespace

}  // namespace lis3mdl
}  // namespace hw_drivers
