#pragma once

#include <algorithm>
#include <bit>
#include <cstdint>
#include <expected>

#include "pw_i2c/register_device.h"

#include "hw_drivers/lis3mdl/lis3mdl.emb.h"
#include "hw_drivers/lis3mdl/lis3mdl.pb.h"

namespace hw_drivers {
namespace lis3mdl {

// XXX: static or not?
constexpr uint32_t kFullScale4LSBPerGauss = 6842;
constexpr uint32_t kFullScale8LSBPerGauss = 3421;
constexpr uint32_t kFullScale12LSBPerGauss = 2281;
constexpr uint32_t kFullScale16LSBPerGauss = 1711;
// XXX: Better way to define all of these various constants?
// - this one is a bit annoying that the math doesn't quite work out.
// - [ ] Test that magnitude remains same when changing full scale.


enum class ConfigurationError {
  // Config is not valid, eg) missing expected parameters
  kInvalidConfig,
  // Config is not supportable with the hardware
  kUnsupportedConfig,
};


struct LIS3MDLData {
  public:
    DataView GetView();

    std::array<std::byte, Data::MaxSizeInBytes()> bytes {std::byte{0}};
};

struct LIS3MDLControl {
  public:
    std::array<std::byte, Control::MaxSizeInBytes()> bytes {std::byte{0}};
};

// XXX: Move to util
// template<size_t N, typename T>
//
// constant_integer<N> array_size( const std::array<T, N>& );


// XXX:
//
// - function to compute reading based on settings and DataView
// - maybe start math functions to handle these
//
// - [ ] may be try to detect bounding issue if not "locked"
//   - I no longer know what ^ means


// XXX: Setup error result support ... -> std::expected!

// XXX: This templating is annoying / requiring in .h
// template <typename OtherStorage>
// std::expected<LIS3MDLConfiguration, ConfigurationError> SolveConfiguration(const LIS3MDLConfiguration& desired_configuration,
//     GenericControlView<OtherStorage>* control);
//  Switched to adding a wrapper class that owns the data to change it :shrug:

// XXX: clang-format plz
//
// XXX: Support strict mode where desired must match actual (in a top-level
// function)
std::expected<LIS3MDLConfiguration, ConfigurationError> SolveConfiguration(const LIS3MDLConfiguration& desired_configuration,
    LIS3MDLControl* control); 

LIS3MDLReading InterpretReading(uint32_t lsb_per_gauss,
    const LIS3MDLData& data);

// XXX: return status, pass in i2c objects
pw::Status ApplyControlToDevice(const LIS3MDLControl& control, pw::i2c::RegisterDevice* register_device);
pw::Status ReadFromDevice(LIS3MDLData *data, pw::i2c::RegisterDevice* register_device);



class LIS3MDL {
  public:
};

}
}
