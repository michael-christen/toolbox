#pragma once

#include <algorithm>
#include <bit>
#include <expected>

#include "hw_drivers/lis3mdl/lis3mdl.emb.h"
#include "hw_drivers/lis3mdl/lis3mdl.pb.h"

namespace hw_drivers {
namespace lis3mdl {


enum class ConfigurationError {
  // Config is not valid, eg) missing expected parameters
  kInvalidConfig,
  // Config is not supportable with the hardware
  kUnsupportedConfig,
};


// XXX:
// - "solve" configuration and test that
// - function to go from configuration to ControlView
//   - maybe include in same thing
//
// - function to compute reading based on settings and DataView
// - maybe start math functions to handle these
//
// - [ ] may be try to detect bounding issue if not "locked"


// XXX: Setup error result support ...
//

// XXX: This templating is annoying / requiring in .h
// template <typename OtherStorage>
// std::expected<LIS3MDLConfiguration, ConfigurationError> SolveConfiguration(const LIS3MDLConfiguration& desired_configuration,
//     GenericControlView<OtherStorage>* control);

// XXX: clang-format plz
//
// XXX: Support strict mode where desired must match actual (in a top-level
// function)
template <typename OtherStorage>
std::expected<LIS3MDLConfiguration, ConfigurationError> SolveConfiguration(const LIS3MDLConfiguration& desired_configuration,
    GenericControlView<OtherStorage>* control) {
  (void) control;  // XXX
  // Constraints of our system:
  // - 
  LIS3MDLConfiguration result_configuration;
  if(!(desired_configuration.has_temperature_enabled() &&
        desired_configuration.has_allowable_rms_noise_ug() &&
        desired_configuration.has_data_rate_millihz() &&
        desired_configuration.has_scale_gauss())) {
    return std::unexpected(ConfigurationError::kInvalidConfig);
  }

  // Temperature
  result_configuration.set_temperature_enabled(desired_configuration.temperature_enabled());
  // RMS Noise and OperatingMode
  auto desired_rms_noise_ug = desired_configuration.allowable_rms_noise_ug();
  uint32_t actual_rms_noise_ug;
  OperatingMode operating_mode;
  if (desired_rms_noise_ug < 3'500) {
    return std::unexpected(ConfigurationError::kUnsupportedConfig);
  } else if (desired_rms_noise_ug < 4'000) {
    actual_rms_noise_ug = 3'500;
    operating_mode = OperatingMode::OPERATING_MODE_ULTRA_HIGH_PERFORMANCE;
  } else if (desired_rms_noise_ug < 4'600) {
    actual_rms_noise_ug = 4'000;
    operating_mode = OperatingMode::OPERATING_MODE_HIGH_PERFORMANCE;
  } else if (desired_rms_noise_ug < 5'300) {
    actual_rms_noise_ug = 4'600;
    operating_mode = OperatingMode::OPERATING_MODE_MEDIUM_PERFORMANCE;
  } else {
    actual_rms_noise_ug = 5'300;
    operating_mode = OperatingMode::OPERATING_MODE_LOW_POWER;
  }
  result_configuration.set_allowable_rms_noise_ug(actual_rms_noise_ug);

  // Date Rate Configuration
  auto desired_data_rate_millihz = desired_configuration.data_rate_millihz();
  constexpr uint32_t kBaseRate = 625;
  // kBaseRate * 2 ^ exponent = frequency
  // exponent = log2(frequency / kBaseRate)
  // log2 for integer is just the position of the highest bit, which we get
  // with std::bit-width(...) - 1
  constexpr uint32_t kMaxExponent = 7;
  uint32_t multiple_of_base = desired_data_rate_millihz / kBaseRate;
  // 0 is invalid, we've got to have at least have 1 when we take log2
  multiple_of_base = std::max(static_cast<uint32_t>(1), multiple_of_base);
  uint32_t exponent = std::bit_width(multiple_of_base) - 1;
  uint32_t actual_data_rate_millihz;
  bool fast_output_data_rate;
  if (exponent <= kMaxExponent) {
    // kBaseRate * 2 ^ exponent = frequency (use bit-shifts to adjust)
    actual_data_rate_millihz = kBaseRate << exponent;
    fast_output_data_rate = false;
  } else {
    fast_output_data_rate = true;
    // XXX: What happens if we set exponent > 7 to our bitfield?
    exponent = 7;
    switch (operating_mode) {
      case OperatingMode::OPERATING_MODE_LOW_POWER:
        actual_data_rate_millihz = 1'000'000;
        break;
      case OperatingMode::OPERATING_MODE_MEDIUM_PERFORMANCE:
        actual_data_rate_millihz = 560'000;
        break;
      case OperatingMode::OPERATING_MODE_HIGH_PERFORMANCE:
        actual_data_rate_millihz = 300'000;
        break;
      case OperatingMode::OPERATING_MODE_ULTRA_HIGH_PERFORMANCE:
        actual_data_rate_millihz = 155'000;
        break;
    }
  }
  result_configuration.set_data_rate_millihz(actual_data_rate_millihz);


  // Scale Gauss
  // XXX: Note that this selection is kinda the opposite of the rms noise
  auto desired_scale_gauss = desired_configuration.scale_gauss();
  uint32_t actual_scale_gauss;
  FullScaleSelection full_scale_choice;
  if (desired_scale_gauss <= 4) {
    actual_scale_gauss = 4;
    full_scale_choice = FullScaleSelection::FULL_SCALE_SELECTION_4;
  } else if (desired_scale_gauss <= 8) {
    actual_scale_gauss = 8;
    full_scale_choice = FullScaleSelection::FULL_SCALE_SELECTION_8;
  } else if (desired_scale_gauss <= 12) {
    actual_scale_gauss = 12;
    full_scale_choice = FullScaleSelection::FULL_SCALE_SELECTION_12;
  } else {
    actual_scale_gauss = 16;
    full_scale_choice = FullScaleSelection::FULL_SCALE_SELECTION_16;
  }
  result_configuration.set_scale_gauss(actual_scale_gauss);



  // Ensure full result before applying to control
  control->temperature_enable().Write(result_configuration.temperature_enabled());
  control->full_scale().Write(full_scale_choice);
  control->xy_axis_operating_mode().Write(operating_mode);
  control->z_axis_operating_mode().Write(operating_mode);
  control->output_data_rate().Write(exponent);
  control->fast_output_data_rate().Write(fast_output_data_rate);


  return result_configuration;
}


class LIS3MDL {
  public:
};

}
}
