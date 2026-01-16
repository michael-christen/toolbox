#include <cstdint>

#include "hw_drivers/lsm6dso/lsm6dso.emb.h"

namespace hw_drivers {
namespace lsm6dso {

// XXX: Convert to unit-test
// XXX: Simpler bit-fields may be preferable
bool Example() {
  uint8_t data = 0b0;
  constexpr uint8_t k1Byte = 1;
  auto msg_view = MakeFuncCfgAccessView(&data, k1Byte);
  if (!msg_view.IsComplete()) {
    return false;
  }
  return msg_view.func_cfg_access().Read() && msg_view.shub_reg_access().Read();
}

}  // namespace lsm6dso
}  // namespace hw_drivers
