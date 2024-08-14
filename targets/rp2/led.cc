// Copyright 2024 The Pigweed Authors
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may not
// use this file except in compliance with the License. You may obtain a copy of
// the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations under
// the License.

#include "pico/stdlib.h"
#include "pw_digital_io_rp2040/digital_io.h"
#include "system/system.h"

namespace demo::system {

static constexpr pw::digital_io::Rp2040Config kDefaultLedConfig = {
    .pin = PICO_DEFAULT_LED_PIN,
    .polarity = pw::digital_io::Polarity::kActiveHigh,
};

pw::digital_io::DigitalInOut& MonochromeLed() {
  static ::pw::digital_io::Rp2040DigitalInOut led_sio(kDefaultLedConfig);
  return led_sio;
}

}  // namespace demo::system
