#include "hw_drivers/lis3mdl/lis3mdl.h"

#include <expected>

namespace hw_drivers {
namespace lis3mdl {

namespace {
constexpr std::chrono::milliseconds kI2cTimeout{100};
}

std::expected<::hw_drivers_lis3mdl_LIS3MDLConfiguration, ConfigurationError>
SolveConfiguration(
    const ::hw_drivers_lis3mdl_LIS3MDLConfiguration& desired_configuration,
    LIS3MDLControl* control) {
  auto view = MakeControlView(control->bytes.data(), std::size(control->bytes));
  // Constraints of our system:
  // -
  if (!(desired_configuration.has_temperature_enabled &&
        desired_configuration.has_allowable_rms_noise_ug &&
        desired_configuration.has_data_rate_millihz &&
        desired_configuration.has_scale_gauss)) {
    return std::unexpected(ConfigurationError::kInvalidConfig);
  }

  // RMS Noise and OperatingMode
  auto desired_rms_noise_ug = desired_configuration.allowable_rms_noise_ug;
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

  // Date Rate Configuration
  auto desired_data_rate_millihz = desired_configuration.data_rate_millihz;
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

  // Scale Gauss
  // Note that this selection is kinda the opposite of the rms noise
  auto desired_scale_gauss = desired_configuration.scale_gauss;
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
  ::hw_drivers_lis3mdl_LIS3MDLConfiguration result_configuration{
      .has_temperature_enabled = true,
      // Temperature
      .temperature_enabled = desired_configuration.temperature_enabled,
      .has_allowable_rms_noise_ug = true,
      .allowable_rms_noise_ug = actual_rms_noise_ug,
      .has_data_rate_millihz = true,
      .data_rate_millihz = actual_data_rate_millihz,
      .has_scale_gauss = true,
      .scale_gauss = actual_scale_gauss,
  };

  // Ensure full result before applying to control
  view.temperature_enable().Write(result_configuration.temperature_enabled);
  view.full_scale().Write(full_scale_choice);
  view.xy_axis_operating_mode().Write(operating_mode);
  view.z_axis_operating_mode().Write(operating_mode);
  view.output_data_rate().Write(exponent);
  view.fast_output_data_rate().Write(fast_output_data_rate);
  view.block_data_update().Write(true);

  return result_configuration;
}

::hw_drivers_lis3mdl_LIS3MDLReading InterpretReading(uint32_t lsb_per_gauss,
                                                     const LIS3MDLData& data) {
  ::hw_drivers_lis3mdl_LIS3MDLReading reading;
  auto view = MakeDataView(data.bytes.data(), std::size(data.bytes));

  reading.has_data_fresh = true;
  reading.data_fresh = view.zyxd_available().Read();
  reading.has_data_overrun = true;
  reading.data_overrun = view.zyx_overrun().Read();

  // 0 = 25C
  // LSB = 1/8 C = 1.25 dC = 125 mC
  // We operate in mC then scale down to dC at the end.
  constexpr int32_t kOffsetTemperatureMC = 25'000;
  constexpr int32_t kTemperatureMCPerLSB = 125;
  constexpr int32_t kMilliPerDeci = 100;
  reading.has_temperature_dc = true;
  reading.temperature_dc =
      (((view.temperature_out().Read() * kTemperatureMCPerLSB) +
        kOffsetTemperatureMC) /
       kMilliPerDeci);

  reading.has_magnetic_strength_x_ug = true;
  reading.has_magnetic_strength_y_ug = true;
  reading.has_magnetic_strength_z_ug = true;
  reading.magnetic_strength_x_ug =
      ((static_cast<int64_t>(view.out_x().Read()) * 1'000'000) / lsb_per_gauss);
  reading.magnetic_strength_y_ug =
      ((static_cast<int64_t>(view.out_y().Read()) * 1'000'000) / lsb_per_gauss);
  reading.magnetic_strength_z_ug =
      ((static_cast<int64_t>(view.out_z().Read()) * 1'000'000) / lsb_per_gauss);
  return reading;
}

pw::Status ApplyControlToDevice(const LIS3MDLControl& control,
                                pw::i2c::RegisterDevice* register_device) {
  // TODO(#144): Could I do something differently and avoid the extra buffer?
  // - I could make a LIS3MDLControl that is "wrong" and the first value is the
  // address?
  std::array<std::byte, Control::MaxSizeInBytes() + 1> raw_buf = {std::byte{0}};
  auto buf = pw::as_writable_bytes(pw::span(raw_buf));
  return register_device->WriteRegisters(
      static_cast<uint8_t>(RegisterAddress::CONTROL), pw::span(control.bytes),
      buf, kI2cTimeout);
}

pw::Status ReadFromDevice(LIS3MDLData* data,
                          pw::i2c::RegisterDevice* register_device) {
  return register_device->ReadRegisters(
      static_cast<uint8_t>(RegisterAddress::DATA), pw::span(data->bytes),
      kI2cTimeout);
}

std::expected<uint32_t, ConfigurationError> GetLsbPerGauss(
    uint32_t scale_gauss) {
  switch (scale_gauss) {
    case 4:
      return kFullScale4LSBPerGauss;
    case 8:
      return kFullScale8LSBPerGauss;
    case 12:
      return kFullScale12LSBPerGauss;
    case 16:
      return kFullScale16LSBPerGauss;
    default:
      return std::unexpected(ConfigurationError::kInvalidConfig);
  }
}

}  // namespace lis3mdl
}  // namespace hw_drivers
