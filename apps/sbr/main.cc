#define PW_LOG_MODULE_NAME "MAIN"

#include "apps/sbr/system/system.h"
#include "hw_services/sbr/service.h"
#include "pw_log/log.h"
#include "pw_system/system.h"

int main() {
  apps::sbr::system::Init();

  auto& rpc_server = pw::System().rpc_server();

  static hw_services::sbr::SbrService sbr_service;

  auto& reg_device = apps::sbr::system::LIS3MDLRegisterDevice();
  sbr_service.Init(pw::System().dispatcher(), pw::System().allocator(),
                   &reg_device);
  rpc_server.RegisterService(sbr_service);

  PW_LOG_INFO("Started SBR app; waiting for RPCs...");
  apps::sbr::system::Start();
  PW_UNREACHABLE;
}
