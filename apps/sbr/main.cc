#define PW_LOG_MODULE_NAME "MAIN"

#include "hw_service/sbr/service.h"
#include "pw_log/log.h"
#include "pw_system/system.h"
#include "apps/sbr/system/system.h"

int main() {
  apps::sbr::system::Init();
  auto& rpc_server = pw::System().rpc_server();

  // XXX: Replace blilnky service
  static hw_service::sbr::SbrService sbr_service;
  sbr_service.Init(
      pw::System().dispatcher(), pw::System().allocator());
  rpc_server.RegisterService(sbr_service);

  PW_LOG_INFO("Started SBR app; waiting for RPCs...");
  apps::sbr::system::Start();
  PW_UNREACHABLE;
}
