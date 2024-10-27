
// XXX: clang-format plz
LIS3MDLConfiguration SolveConfiguration(const LIS3MDLConfiguration& desired_configuration,
    ControlView* control) {
  // Constraints of our system:
  // - 
  LIS3MDLConfiguration result_configuration;
  if(desired_configuration.has_temperature_enabled()) {
    result_configuration.set_temperature_enabled(desired_configuration.temperature_enabled());
  }
}
