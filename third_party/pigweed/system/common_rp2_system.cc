#include "hardware/adc.h"
#include "hardware/exception.h"
#include "pico/stdlib.h"
#include "pw_cpu_exception/entry.h"

#if defined(PICO_RP2040) && PICO_RP2040
#include "system_RP2040.h"
#endif  // defined(PICO_RP2040) && PICO_RP2040
#if defined(PICO_RP2350) && PICO_RP2350
#include "system_RP2350.h"
#endif  // defined(PICO_RP2350) && PICO_RP2350
        //
namespace third_party {
namespace pigweed {
namespace system {

// Initialize PICO_SDK
void CommonRp2Init() {
  // PICO_SDK inits.
  SystemInit();
  stdio_init_all();
  setup_default_uart();
  stdio_usb_init();
  adc_init();

  // Install the CPU exception handler.
  exception_set_exclusive_handler(HARDFAULT_EXCEPTION, pw_cpu_exception_Entry);
}

}  // namespace system
}  // namespace pigweed
}  // namespace third_party
