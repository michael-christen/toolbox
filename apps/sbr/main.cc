#define PW_LOG_MODULE_NAME "MAIN"

#include "apps/sbr/system/system.h"
#include "pw_log/log.h"
#include "pw_system/system.h"

int main() {
  apps::sbr::system::Init();
  auto& rpc_server = pw::System().rpc_server();

  PW_LOG_INFO("Started SBR app; waiting for RPCs...");
  apps::sbr::system::Start();
  PW_UNREACHABLE;
}
