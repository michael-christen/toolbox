
#define PW_LOG_MODULE_NAME "MAIN"

#include "pw_board_led/led.h"
#include "pw_chrono/system_clock.h"
#include "pw_chrono/system_timer.h"
#include "pw_log/log.h"
#include "pw_system/work_queue.h"

namespace {

using namespace ::std::chrono_literals;

void ToggleLedCallback(pw::chrono::SystemClock::time_point);

pw::chrono::SystemTimer blink_timer(ToggleLedCallback);

void ScheduleLedToggle() { blink_timer.InvokeAfter(1s); }

void ToggleLedCallback(pw::chrono::SystemClock::time_point) {
  PW_LOG_INFO("Toggling LED");
  pw::board_led::Toggle();
  // Scheduling the timer again might not be safe from this context, so instead
  // just defer to the work queue.
  pw::system::GetWorkQueue().PushWork(ScheduleLedToggle);
}

}  // namespace

namespace pw::system {

// This will run once after pw::system::Init() completes. This callback must
// return or it will block the work queue.
void UserAppInit() {
  pw::board_led::Init();
  // Start the blink cycle.
  pw::system::GetWorkQueue().PushWork(ScheduleLedToggle);
}

}  // namespace pw::system
