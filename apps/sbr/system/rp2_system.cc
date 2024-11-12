#include "apps/sbr/system/system.h"

#include "third_party/pigweed/system/common_rp2_system.h"

// XXX: Decide on namespace style
namespace apps::sbr::system {

void Init() {
  third_party::pigweed::system::CommonRp2Init();
}

void Start() {
  PW_RP2_SYSTEM_START(2048)
}

}  // namespace apps::sbr::system
