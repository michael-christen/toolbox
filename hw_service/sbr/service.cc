
#define PW_LOG_MODULE_NAME "SBR"

#include "pw_log/log.h"
#include "hw_service/sbr/service.h"

namespace hw_service {
namespace sbr {

void SbrService::Init(pw::async2::Dispatcher& dispatcher,
          pw::Allocator& allocator) {
  (void) dispatcher;
  (void) allocator;
}

pw::Status SbrService::ConfigureMagnetometer(const hw_drivers_lis3mdl_LIS3MDLConfiguration& config, hw_drivers_lis3mdl_LIS3MDLConfiguration& actual_config) {
  (void) config;
  (void) actual_config;
  PW_LOG_INFO("CONFIGURE MAGNETOMETER");
  // XXX: What's not implemented?
  return pw::OkStatus();
};

pw::Status SbrService::ReadMagnetometer(const pw_protobuf_Empty&, hw_drivers_lis3mdl_LIS3MDLReading& reading) {
  (void) reading;
  PW_LOG_INFO("READ MAGNETOMETER");
  // XXX: What's not implemented?
  return pw::OkStatus();
}

}
}
