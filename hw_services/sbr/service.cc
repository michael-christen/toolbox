
#define PW_LOG_MODULE_NAME "SBR"

#include "hw_services/sbr/service.h"

#include "hw_drivers/lis3mdl/lis3mdl.emb.h"
#include "hw_drivers/lis3mdl/lis3mdl.h"
#include "pw_assert/check.h"
#include "pw_log/log.h"

namespace hw_services {
namespace sbr {

void SbrService::Init(pw::async2::Dispatcher& dispatcher,
                      pw::Allocator& allocator,
                      pw::i2c::RegisterDevice* register_device) {
  (void)dispatcher;
  (void)allocator;
  register_device_ = register_device;
}

pw::Status SbrService::ConfigureMagnetometer(
    const hw_drivers_lis3mdl_LIS3MDLConfiguration& config,
    hw_drivers_lis3mdl_LIS3MDLConfiguration& actual_config) {
  PW_CHECK(register_device_.has_value());

  PW_LOG_INFO("CONFIGURE MAGNETOMETER");
  hw_drivers::lis3mdl::LIS3MDLControl control;
  auto result = hw_drivers::lis3mdl::SolveConfiguration(config, &control);
  if (result.has_value()) {
    actual_config = result.value();
    auto application_result = hw_drivers::lis3mdl::ApplyControlToDevice(control,
                                                     register_device_.value());
    if (application_result.ok()) {
      cached_config_ = config;
    }
    return application_result;
  } else {
    switch (result.error()) {
      case hw_drivers::lis3mdl::ConfigurationError::kInvalidConfig:
        return pw::Status::InvalidArgument();
      case hw_drivers::lis3mdl::ConfigurationError::kUnsupportedConfig:
        return pw::Status::OutOfRange();
    }
  }
};

pw::Status SbrService::ReadMagnetometer(
    const pw_protobuf_Empty&, hw_drivers_lis3mdl_LIS3MDLReading& reading) {
  PW_CHECK(register_device_.has_value());
  if (!cached_config_.has_scale_gauss) {
    return pw::Status::FailedPrecondition();
  }
  auto lsb_per_gauss = hw_drivers::lis3mdl::GetLsbPerGauss(cached_config_.scale_gauss);
  if (!lsb_per_gauss.has_value()) {
    return pw::Status::FailedPrecondition();
  }

  PW_LOG_INFO("READ MAGNETOMETER");
  hw_drivers::lis3mdl::LIS3MDLData data;
  auto status =
      hw_drivers::lis3mdl::ReadFromDevice(&data, register_device_.value());
  if (!status.ok()) {
    return status;
  }
  reading = hw_drivers::lis3mdl::InterpretReading(
      lsb_per_gauss.value(), data);
  return pw::OkStatus();
}

}  // namespace sbr
}  // namespace hw_services
