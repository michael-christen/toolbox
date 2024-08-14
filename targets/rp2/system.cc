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

#include "system/system.h"

#include "hardware/adc.h"
#include "hardware/exception.h"
#include "pico/stdlib.h"
#include "pw_channel/rp2_stdio_channel.h"
#include "pw_cpu_exception/entry.h"
#include "pw_digital_io_rp2040/digital_io.h"
#include "pw_multibuf/simple_allocator.h"
#include "pw_system/system.h"
#if defined(PICO_RP2040) && PICO_RP2040
#include "system_RP2040.h"
#endif  // defined(PICO_RP2040) && PICO_RP2040
#if defined(PICO_RP2350) && PICO_RP2350
#include "system_RP2350.h"
#endif  // defined(PICO_RP2350) && PICO_RP2350

using pw::digital_io::Rp2040DigitalIn;

namespace demo::system {

void Init() {
  // PICO_SDK inits.
  SystemInit();
  stdio_init_all();
  setup_default_uart();
  stdio_usb_init();
  adc_init();

  // Install the CPU exception handler.
  exception_set_exclusive_handler(HARDFAULT_EXCEPTION, pw_cpu_exception_Entry);
}

void Start() {
  static std::byte channel_buffer[2048];
  static pw::multibuf::SimpleAllocator multibuf_alloc(channel_buffer,
                                                      pw::System().allocator());
  pw::SystemStart(pw::channel::Rp2StdioChannelInit(multibuf_alloc));
  PW_UNREACHABLE;
}

}  // namespace demo::system
