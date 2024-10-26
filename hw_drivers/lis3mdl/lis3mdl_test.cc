#include <catch2/catch_test_macros.hpp>

#include <cstdint>

#include "hw_drivers/lis3mdl/lis3mdl.emb.h"

namespace hw_drivers {
namespace lis3mdl {

TEST_CASE("offset") {
  uint8_t buf[8];

  // XXX: Failing static assertion
  auto offset_view = MakeOffsetView(buf, sizeof(buf));
  offset_view.out_x().Write(0x1234);

  REQUIRE(offset_view.out_x().Read() == 0x1234);
  REQUIRE(buf[0] == 0x34);
  REQUIRE(buf[1] == 0x10);
}

TEST_CASE("emboss and calculations are correct") {
  // XXX: use size of Control
  uint8_t buf[12];

  auto control_view = MakeControlView(buf, sizeof(buf));
  control_view.temperature_enable().Write(true);

  REQUIRE(control_view.temperature_enable().Read());
  REQUIRE(buf[0] & 0x80);
}

}
}
