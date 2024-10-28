#include "hw_drivers/lis3mdl/lis3mdl.h"

#include <cstdint>
#include <vector>

#include <catch2/catch_test_macros.hpp>

#include "hw_drivers/lis3mdl/lis3mdl.emb.h"
#include "hw_drivers/lis3mdl/lis3mdl.pb.h"


namespace hw_drivers {
namespace lis3mdl {

namespace {

TEST_CASE("offset") {
  uint8_t buf[Offset::MaxSizeInBytes()];

  auto offset_view = MakeOffsetView(buf, sizeof(buf));
  offset_view.out_x().Write(0x1234);

  CHECK(offset_view.out_x().Read() == 0x1234);
  CHECK(buf[0] == 0x34);
  CHECK(buf[1] == 0x12);
}

TEST_CASE("emboss and calculations are correct") {
  uint8_t buf[Control::MaxSizeInBytes()];

  auto control_view = MakeControlView(buf, sizeof(buf));
  control_view.temperature_enable().Write(true);

  CHECK(control_view.temperature_enable().Read());
  CHECK(buf[0] & 0x80);
}

// XXX: probably have to use nanopb syntax?
TEST_CASE("SolveConfiguration") {
  LIS3MDLConfiguration configuration;
  // XXX: Better naming schema to denote differences
  // XXX: Analysis on size and run-time cost
  LIS3MDLControl control;
  auto control_view = MakeControlView(control.bytes, sizeof(control.bytes));
  auto result = SolveConfiguration(configuration, &control);
  REQUIRE(!result.has_value());
  CHECK(result.error() == ConfigurationError::kInvalidConfig);

  configuration.set_temperature_enabled(false);
  configuration.set_allowable_rms_noise_ug(3'500);
  configuration.set_data_rate_millihz(80'000);
  configuration.set_scale_gauss(4);

  result = SolveConfiguration(configuration, &control);
  REQUIRE(result.has_value());
  auto actual_config = result.value();
  // XXX: Better protobuf comparison
  REQUIRE(actual_config.has_temperature_enabled());
  CHECK(!actual_config.temperature_enabled());
  CHECK(!control_view.temperature_enable().Read());

  // Test Plan:
  // - rms noise coverage
  // - check math on frequency decision / can I break it?
}

TEST_CASE("Read Data") {
  // XXX: Max or Intrinsic?
  static_assert(Data::MaxSizeInBytes() == 9);
  static_assert(Data::IntrinsicSizeInBytes() == 9);

  LIS3MDLData d;
  auto view = MakeDataView(d.bytes, sizeof(d.bytes));

  // Check simple available / overrun behavior
  view.zyxd_available().Write(1);
  view.zyx_overrun().Write(1);
  auto reading = InterpretReading(kFullScale4LSBPerGauss, d);
  CHECK(reading.data_fresh());
  CHECK(reading.data_overrun());

  view.zyx_overrun().Write(0);
  reading = InterpretReading(kFullScale4LSBPerGauss, d);
  CHECK(reading.data_fresh());
  CHECK(!reading.data_overrun());

  view.zyxd_available().Write(0);
  reading = InterpretReading(kFullScale4LSBPerGauss, d);
  CHECK(!reading.data_fresh());
  CHECK(!reading.data_overrun());

  // Check Temperature
  view.temperature_out().Write(0);
  reading = InterpretReading(kFullScale4LSBPerGauss, d);
  CHECK(reading.temperature_dc() == 250);
  // XXX: Check more
  
  view.out_x().Write(-100);
  view.out_y().Write(0);
  view.out_z().Write(200);
  reading = InterpretReading(kFullScale4LSBPerGauss, d);
  CHECK(reading.magnetic_strength_ug().at(0) == -14'615);
  CHECK(reading.magnetic_strength_ug().at(1) == 0);
  CHECK(reading.magnetic_strength_ug().at(2) == 29'231);

  // Changing scale changes the behavior (eye-balled around 4x)
  reading = InterpretReading(kFullScale16LSBPerGauss, d);
  CHECK(reading.magnetic_strength_ug().at(0) == -58'445);
  CHECK(reading.magnetic_strength_ug().at(1) == 0);
  CHECK(reading.magnetic_strength_ug().at(2) == 116'890);
}

}

}
}
