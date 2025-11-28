
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

  hw_drivers::lis3mdl::LIS3MDLControl control;
  auto result = hw_drivers::lis3mdl::SolveConfiguration(config, &control);
  if (std::holds_alternative<hw_drivers_lis3mdl_LIS3MDLConfiguration>(result)) {
    actual_config = std::get<hw_drivers_lis3mdl_LIS3MDLConfiguration>(result);
    auto application_result = hw_drivers::lis3mdl::ApplyControlToDevice(
        control, register_device_.value());
    if (application_result.ok()) {
      cached_config_ = config;
    }
    return application_result;
  } else if (std::holds_alternative<::hw_drivers::lis3mdl::ConfigurationError>(
                 result)) {
    switch (std::get<::hw_drivers::lis3mdl::ConfigurationError>(result)) {
      case hw_drivers::lis3mdl::ConfigurationError::kInvalidConfig:
        return pw::Status::InvalidArgument();
      case hw_drivers::lis3mdl::ConfigurationError::kUnsupportedConfig:
        return pw::Status::OutOfRange();
    }
  } else {
    PW_CRASH("Impossible condition for a variant");
  }
};

pw::Status SbrService::ReadMagnetometer(
    const pw_protobuf_Empty&, hw_drivers_lis3mdl_LIS3MDLReading& reading) {
  PW_CHECK(register_device_.has_value());
  if (!cached_config_.has_scale_gauss) {
    return pw::Status::FailedPrecondition();
  }
  auto lsb_per_gauss =
      hw_drivers::lis3mdl::GetLsbPerGauss(cached_config_.scale_gauss);
  if (!std::holds_alternative<uint32_t>(lsb_per_gauss)) {
    return pw::Status::FailedPrecondition();
  }

  hw_drivers::lis3mdl::LIS3MDLData data;
  auto status =
      hw_drivers::lis3mdl::ReadFromDevice(&data, register_device_.value());
  if (!status.ok()) {
    return status;
  }
  reading = hw_drivers::lis3mdl::InterpretReading(
      std::get<uint32_t>(lsb_per_gauss), data);
  return pw::OkStatus();
}

}  // namespace sbr
}  // namespace hw_services
