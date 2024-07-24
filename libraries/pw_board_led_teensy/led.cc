// Copyright 2020 The Pigweed Authors
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

#include <Arduino.h>

#include <cinttypes>

// pw::board_led API implementation for the Teensy 3.x and 4.x using the Arduino
// digitalWrite function.
namespace pw::board_led {
namespace {

constexpr int kLedPin = 13;
bool led_on = false;

}  // namespace

void Init() {
  pinMode(kLedPin, OUTPUT);
  TurnOff();
}

void TurnOff() {
  digitalWrite(kLedPin, LOW);
  led_on = false;
}

void TurnOn() {
  digitalWrite(kLedPin, HIGH);
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
