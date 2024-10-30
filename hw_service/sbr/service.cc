
#define PW_LOG_MODULE_NAME "SBR"

#include "pw_log/log.h"
#include "hw_service/sbr/service.h"
#include "hw_drivers/lis3mdl/lis3mdl.h"
#include "hw_drivers/lis3mdl/lis3mdl.emb.h"

namespace hw_service {
namespace sbr {

void SbrService::Init(pw::async2::Dispatcher& dispatcher,
          pw::Allocator& allocator) {
  (void) dispatcher;
  (void) allocator;
}

pw::Status SbrService::ConfigureMagnetometer(const hw_drivers_lis3mdl_LIS3MDLConfiguration& config, hw_drivers_lis3mdl_LIS3MDLConfiguration& actual_config) {
  PW_LOG_INFO("CONFIGURE MAGNETOMETER");
  hw_drivers::lis3mdl::LIS3MDLControl control;
  auto result = hw_drivers::lis3mdl::SolveConfiguration(
      config, &control);
  if (result.has_value()) {
    actual_config = result.value();
    return pw::OkStatus();
  } else {
    switch (result.error()) {
      case hw_drivers::lis3mdl::ConfigurationError::kInvalidConfig:
        return pw::Status::InvalidArgument();
      case hw_drivers::lis3mdl::ConfigurationError::kUnsupportedConfig:
        return pw::Status::OutOfRange();
    }
  }
};

pw::Status SbrService::ReadMagnetometer(const pw_protobuf_Empty&, hw_drivers_lis3mdl_LIS3MDLReading& reading) {
  PW_LOG_INFO("READ MAGNETOMETER");
  hw_drivers::lis3mdl::LIS3MDLData data;
  // auto status = hw_drivers::lis3mdl::ReadFromDevice(&data, &register_device);
  reading = hw_drivers::lis3mdl::InterpretReading(hw_drivers::lis3mdl::kFullScale4LSBPerGauss, data);
  return pw::OkStatus();
}

}
}
