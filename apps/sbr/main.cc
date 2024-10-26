#define PW_LOG_MODULE_NAME "MAIN"

#include "examples/pigweed/modules/blinky/service.h"
#include "pw_log/log.h"
#include "pw_system/system.h"
#include "examples/pigweed/system/system.h"

int main() {
  demo::system::Init();
  auto& rpc_server = pw::System().rpc_server();
  auto& monochrome_led = demo::system::MonochromeLed();

  // XXX: Replace blilnky service
  static demo::BlinkyService blinky_service;
  blinky_service.Init(
      pw::System().dispatcher(), pw::System().allocator(), monochrome_led);
  rpc_server.RegisterService(blinky_service);

  PW_LOG_INFO("Started blinky app; waiting for RPCs...");
  demo::system::Start();
  PW_UNREACHABLE;
}

