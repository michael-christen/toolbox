#include "apps/sbr/system/system.h"

#include "third_party/pigweed/system/common_host_system.h"

namespace apps {
namespace sbr {
namespace system {

void Init() {}

void Start() {
  // third_party::pigweed::system::
  PW_HOST_SYSTEM_START(16384, "//apps/sbr:simulator_console")
}

}  // namespace system
}  // namespace sbr
}  // namespace apps
