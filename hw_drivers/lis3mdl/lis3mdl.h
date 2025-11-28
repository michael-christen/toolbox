#pragma once

#include <algorithm>
#include <bit>
#include <cstdint>
#include <variant>

#include "hw_drivers/lis3mdl/lis3mdl.emb.h"
#include "hw_drivers/lis3mdl/lis3mdl.pb.h"
#include "pw_i2c/address.h"
#include "pw_i2c/register_device.h"

namespace hw_drivers {
namespace lis3mdl {

static constexpr pw::i2c::Address kHighAddress =
    pw::i2c::Address::SevenBit<0b001'1110>();
static constexpr pw::i2c::Address kLowAddress =
    pw::i2c::Address::SevenBit<0b001'1100>();

static constexpr uint32_t kFullScale4LSBPerGauss = 6842;
static constexpr uint32_t kFullScale8LSBPerGauss = 3421;
static constexpr uint32_t kFullScale12LSBPerGauss = 2281;
static constexpr uint32_t kFullScale16LSBPerGauss = 1711;

// Thin wrapper around lis3mdl.emb.h Data to own the data
struct LIS3MDLData {
 public:
  std::array<std::byte, Data::MaxSizeInBytes()> bytes{std::byte{0}};
};

// Thin wrapper around lis3mdl.emb.h Control to own the data
struct LIS3MDLControl {
 public:
  std::array<std::byte, Control::MaxSizeInBytes()> bytes{std::byte{0}};
};

enum class ConfigurationError {
  // Config is not valid, eg) missing expected parameters
  kInvalidConfig,
  // Config is not supportable with the hardware
  kUnsupportedConfig,
};

// Functions to help handle the .proto and .emb objects as well as how to
// interact with an actual i2c device.

// Given a desired_configuration, return the configuration available (or the
// error for why finding a given configuration is not achievable). Also, if
// successful, modify control to have the correct values that fit that
// configuration.
std::variant<hw_drivers_lis3mdl_LIS3MDLConfiguration, ConfigurationError>
SolveConfiguration(
    const ::hw_drivers_lis3mdl_LIS3MDLConfiguration& desired_configuration,
    LIS3MDLControl* control);

// Create a LIS3MDLReading based on data from a device as well as an
// understanding of the scale selected for the device.
::hw_drivers_lis3mdl_LIS3MDLReading InterpretReading(uint32_t lsb_per_gauss,
                                                     const LIS3MDLData& data);

// Apply control to an i2c device
pw::Status ApplyControlToDevice(const LIS3MDLControl& control,
                                pw::i2c::RegisterDevice* register_device);

// Read data from an i2c device
pw::Status ReadFromDevice(LIS3MDLData* data,
                          pw::i2c::RegisterDevice* register_device);

std::variant<uint32_t, ConfigurationError> GetLsbPerGauss(uint32_t scale_gauss);

}  // namespace lis3mdl
}  // namespace hw_drivers
