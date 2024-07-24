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

#include "pw_board_led/led.h"

#include "pico/stdlib.h"

// pw::board_led API implementation for the rp2040 using the pico-sdk.
namespace pw::board_led {
namespace {

constexpr uint kLedPin = PICO_DEFAULT_LED_PIN;
bool led_on = false;

}  // namespace

void Init() {
  gpio_init(kLedPin);
  gpio_set_dir(kLedPin, GPIO_OUT);
  TurnOff();
}

void TurnOff() {
  gpio_put(kLedPin, 0);
  led_on = false;
}

void TurnOn() {
  gpio_put(kLedPin, 1);
  led_on = true;
}

void Toggle() {
  // Check if the LED is on. If so, turn it off.
  if (led_on) {
    TurnOff();
  } else {
    TurnOn();
  }
}

}  // namespace pw::board_led
