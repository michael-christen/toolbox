#include "hw_drivers/lis3mdl/lis3mdl.h"

#include <catch2/catch_test_macros.hpp>

#include <cstdint>

#include "hw_drivers/lis3mdl/lis3mdl.emb.h"
#include "hw_drivers/lis3mdl/lis3mdl.pb.h"

namespace hw_drivers {
namespace lis3mdl {

TEST_CASE("offset") {
  uint8_t buf[Offset::MaxSizeInBytes()];

  auto offset_view = MakeOffsetView(buf, sizeof(buf));
  offset_view.out_x().Write(0x1234);

  REQUIRE(offset_view.out_x().Read() == 0x1234);
  REQUIRE(buf[0] == 0x34);
  REQUIRE(buf[1] == 0x12);
}

TEST_CASE("emboss and calculations are correct") {
  uint8_t buf[Control::MaxSizeInBytes()];

  auto control_view = MakeControlView(buf, sizeof(buf));
  control_view.temperature_enable().Write(true);

  REQUIRE(control_view.temperature_enable().Read());
  REQUIRE(buf[0] & 0x80);
}

// XXX: probably have to use nanopb syntax?
TEST_CASE("SolveConfiguration") {
  LIS3MDLConfiguration configuration;
  // XXX: use size of Control
  // XXX: Max or Intrinsic?
  uint8_t buf[Control::MaxSizeInBytes()];
  auto control_view = MakeControlView(buf, sizeof(buf));
  auto result = SolveConfiguration(configuration, &control_view);
  REQUIRE(!result.has_value());
  REQUIRE(result.error() == ConfigurationError::kInvalidConfig);

  configuration.set_temperature_enabled(false);
  configuration.set_allowable_rms_noise_ug(3'500);
  configuration.set_data_rate_millihz(80'000);
  configuration.set_scale_gauss(4);

  result = SolveConfiguration(configuration, &control_view);
  REQUIRE(result.has_value());
  auto actual_config = result.value();
  // XXX: Better protobuf comparison
  REQUIRE(actual_config.has_temperature_enabled());
  REQUIRE(!actual_config.temperature_enabled());
  REQUIRE(!control_view.temperature_enable().Read());

  // Test Plan:
  // - rms noise coverage
  // - check math on frequency decision / can I break it?
}

}
}
