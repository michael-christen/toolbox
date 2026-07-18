#include <cstdint>

#include "pw_unit_test/framework.h"
#include "tlbox/hw/drivers/lsm6dso/lsm6dso.emb.h"

namespace hw_drivers {
namespace lsm6dso {
namespace {

TEST(Lsm6dsoTest, FuncCfgAccessDefaults) {
  uint8_t data = 0b0;
  constexpr uint8_t k1Byte = 1;
  auto view = MakeFuncCfgAccessView(&data, k1Byte);
  EXPECT_TRUE(view.IsComplete());
  EXPECT_FALSE(view.func_cfg_access().Read());
  EXPECT_FALSE(view.shub_reg_access().Read());
}

TEST(Lsm6dsoTest, FuncCfgAccessBit6) {
  uint8_t data = 0b0100'0000;  // bit 6 set
  constexpr uint8_t k1Byte = 1;
  auto view = MakeFuncCfgAccessView(&data, k1Byte);
  EXPECT_TRUE(view.func_cfg_access().Read());
  EXPECT_FALSE(view.shub_reg_access().Read());
}

TEST(Lsm6dsoTest, ShubRegAccessBit7) {
  uint8_t data = 0b1000'0000;  // bit 7 set
  constexpr uint8_t k1Byte = 1;
  auto view = MakeFuncCfgAccessView(&data, k1Byte);
  EXPECT_FALSE(view.func_cfg_access().Read());
  EXPECT_TRUE(view.shub_reg_access().Read());
}

}  // namespace
}  // namespace lsm6dso
}  // namespace hw_drivers
