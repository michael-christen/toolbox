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

#include <cinttypes>

#include "pw_preprocessor/compiler.h"

// pw::board_led API implementation for the stm32f429i using direct register
// manipulation.
namespace pw::board_led {
namespace {

// Base address for everything peripheral-related on the STM32F4xx.
constexpr uint32_t kPeripheralBaseAddr = 0x40000000u;
// Base address for everything AHB1-related on the STM32F4xx.
constexpr uint32_t kAhb1PeripheralBase = kPeripheralBaseAddr + 0x00020000U;
// Base address for everything APB2-related on the STM32F4xx.
constexpr uint32_t kApb2PeripheralBase = kPeripheralBaseAddr + 0x00010000U;

// Reset/clock configuration block (RCC).
// `reserved` fields are unimplemented features, and are present to ensure
// proper alignment of registers that are in use.
PW_PACKED(struct) RccBlock {
  uint32_t reserved1[12];
  uint32_t ahb1_config;
  uint32_t reserved2[4];
  uint32_t apb2_config;
};

// GPIO register block definition.
PW_PACKED(struct) GpioBlock {
  uint32_t modes;
  uint32_t out_type;
  uint32_t out_speed;
  uint32_t pull_up_down;
  uint32_t input_data;
  uint32_t output_data;
  uint32_t gpio_bit_set;
  uint32_t port_config_lock;
  uint32_t alt_low;
  uint32_t alt_high;
};

// Constants related to GPIO mode register masks.
constexpr uint32_t kGpioPortModeMask = 0x3u;
constexpr uint32_t kGpio13PortModePos = 26;
constexpr uint32_t kGpioPortModeOutput = 1;

// Constants related to GPIO output mode register masks.
constexpr uint32_t kGpioOutputModeMask = 0x1u;
constexpr uint32_t kGpio13OutputModePos = 13;
constexpr uint32_t kGpioOutputModePushPull = 0;

constexpr uint32_t kGpio13BitSetHigh = 0x1u << 13;
constexpr uint32_t kGpio13BitSetLow = kGpio13BitSetHigh << 16;

// Mask for ahb1_config (AHB1ENR) to enable the "G" GPIO pins.
constexpr uint32_t kGpioGEnable = 0x1u << 6;

// Declare a reference to the memory mapped RCC block.
volatile RccBlock& platform_rcc =
    *reinterpret_cast<volatile RccBlock*>(kAhb1PeripheralBase + 0x3800U);

// Declare a reference to the 'G' GPIO memory mapped block.
volatile GpioBlock& gpio_g =
    *reinterpret_cast<volatile GpioBlock*>(kAhb1PeripheralBase + 0x1800U);

}  // namespace

void Init() {
  // Enable 'G' GIPO clocks.
  platform_rcc.ahb1_config |= kGpioGEnable;

  // Enable Pin 13 in output mode.
  gpio_g.modes = (gpio_g.modes & ~(kGpioPortModeMask << kGpio13PortModePos)) |
                 (kGpioPortModeOutput << kGpio13PortModePos);

  // Enable Pin 13 in output mode "push pull"
  gpio_g.out_type =
      (gpio_g.out_type & ~(kGpioOutputModeMask << kGpio13OutputModePos)) |
      (kGpioOutputModePushPull << kGpio13OutputModePos);
}

void TurnOff() { gpio_g.gpio_bit_set = kGpio13BitSetLow; }

void TurnOn() { gpio_g.gpio_bit_set = kGpio13BitSetHigh; }

void Toggle() {
  // Check if the LED is on. If so, turn it off.
  if (gpio_g.output_data & kGpio13BitSetHigh) {
    TurnOff();
  } else {
    TurnOn();
  }
}

}  // namespace pw::board_led
