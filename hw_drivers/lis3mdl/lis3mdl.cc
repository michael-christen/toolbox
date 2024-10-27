#include "hw_drivers/lis3mdl/lis3mdl.h"

#include <expected>

namespace hw_drivers {
namespace lis3mdl {


// XXX: No idea why this is failing / why there's an issue with this
// declaration, but in test code, things are fine ...
DataView LIS3MDLData::GetView() {
  return MakeDataView(bytes, sizeof(bytes));
}


std::expected<LIS3MDLConfiguration, ConfigurationError> SolveConfiguration(const LIS3MDLConfiguration& desired_configuration,
    LIS3MDLControl* control) {
  auto view = MakeControlView(control->bytes, sizeof(control->bytes));
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

  // XXX: I could just do this elsewhere and send the information to write the
  // output separately?
  //
  // Ensure full result before applying to control
  view.temperature_enable().Write(result_configuration.temperature_enabled());
  view.full_scale().Write(full_scale_choice);
  view.xy_axis_operating_mode().Write(operating_mode);
  view.z_axis_operating_mode().Write(operating_mode);
  view.output_data_rate().Write(exponent);
  view.fast_output_data_rate().Write(fast_output_data_rate);

  return result_configuration;
}

// XXX: using lsb_per_gauss, since the scale isn't quite working out how I'd
// expect / the LSBs are not mathing properly
LIS3MDLReading InterpretReading(uint32_t lsb_per_gauss,
                                const LIS3MDLData& data) {
  LIS3MDLReading reading;
  auto view = MakeDataView(data.bytes, sizeof(data.bytes));

  reading.set_data_fresh(view.zyxd_available().Read());
  reading.set_data_overrun(view.zyx_overrun().Read());

  // 0 = 25C
  // LSB = 1/8 C = 1.25 dC = 125 mC
  // We operate in mC then scale down to dC at the end.
  constexpr int32_t kOffsetTemperatureMC = 25'000;
  constexpr int32_t kTemperatureMCPerLSB = 125;
  constexpr int32_t kMilliPerDeci = 100;
  reading.set_temperature_dc(
      ((view.temperature_out().Read() * kTemperatureMCPerLSB) + kOffsetTemperatureMC)
       / kMilliPerDeci);

  constexpr size_t kNumAxes = 3;
  // XXX: Check fixed_size of array
  // static_assert(kNumAxes == );
  int32_t magnetometer_readings[kNumAxes] = {
    view.out_x().Read(),
    view.out_y().Read(),
    view.out_z().Read(),
  };
  // XXX: Any fun new C++ iterable behavior?
  for (size_t i = 0; i < kNumAxes; ++i) {
    reading.mutable_magnetic_strength_ug()->Add(
        (static_cast<int64_t>(magnetometer_readings[i]) * 1'000'000)
        / lsb_per_gauss);
  }
  return reading;
}

}
}
