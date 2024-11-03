#pragma once

// #include "examples/pigweed/modules/blinky/blinky.h"
#include "hw_service/sbr/sbr.rpc.pb.h"
#include "pw_allocator/allocator.h"
#include "pw_async2/dispatcher.h"
#include "pw_i2c/register_device.h"

namespace hw_service {
namespace sbr {

class SbrService final
    : public ::hw_service::sbr::pw_rpc::nanopb::Sbr::Service<SbrService> {
 public:
  void Init(pw::async2::Dispatcher& dispatcher,
            pw::Allocator& allocator,
            pw::i2c::RegisterDevice* register_device);

  pw::Status ConfigureMagnetometer(const hw_drivers_lis3mdl_LIS3MDLConfiguration& config, hw_drivers_lis3mdl_LIS3MDLConfiguration& actual_config);

  pw::Status ReadMagnetometer(const pw_protobuf_Empty&, hw_drivers_lis3mdl_LIS3MDLReading& reading);

 private:
  // XXX: Blinky blinky_;
  std::optional<pw::i2c::RegisterDevice*> register_device_;
};

}
}
