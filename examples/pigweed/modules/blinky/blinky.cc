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
#define PW_LOG_MODULE_NAME "BLINKY"
#include "blinky.h"

#include <mutex>

#include "examples/pigweed/modules/blinky/blinky.h"
#include "pw_async2/coro.h"
#include "pw_log/log.h"

namespace demo {

using ::pw::Allocator;
using ::pw::OkStatus;
using ::pw::Status;
using ::pw::async2::Coro;
using ::pw::async2::CoroContext;
using ::pw::async2::Dispatcher;
using ::pw::digital_io::DigitalInOut;
using ::pw::digital_io::State;

namespace {

bool IsOn(DigitalInOut& io) {
  auto result = io.GetState();
  if (!result.ok()) {
    return false;
  }
  return *result == State::kActive;
}

void TurnOn(DigitalInOut& io) { io.SetState(State::kActive).IgnoreError(); }

void TurnOff(DigitalInOut& io) { io.SetState(State::kInactive).IgnoreError(); }

void ToggleIo(DigitalInOut& io) {
  io.SetState(IsOn(io) ? State::kInactive : State::kActive).IgnoreError();
}

}  // namespace

Coro<Status> Blinky::BlinkLoop(CoroContext&, uint32_t blink_count,
                               pw::chrono::SystemClock::duration interval) {
  for (uint32_t blinked = 0; blinked < blink_count || blink_count == 0;
       ++blinked) {
    {
      PW_LOG_INFO("LED blinking: OFF");
      std::lock_guard lock(lock_);
      TurnOff(*monochrome_led_);
    }
    co_await timer_.WaitFor(interval);
    {
      PW_LOG_INFO("LED blinking: ON");
      std::lock_guard lock(lock_);
      TurnOn(*monochrome_led_);
    }
    co_await timer_.WaitFor(interval);
  }
  {
    std::lock_guard lock(lock_);
    TurnOff(*monochrome_led_);
  }
  PW_LOG_INFO("Stopped blinking");
  co_return OkStatus();
}

Blinky::Blinky()
    : blink_task_(Coro<Status>::Empty(), [](Status) {
        PW_LOG_ERROR("Failed to allocate blink loop coroutine.");
      }) {}

void Blinky::Init(Dispatcher& dispatcher, Allocator& allocator,
                  pw::digital_io::DigitalInOut& monochrome_led) {
  dispatcher_ = &dispatcher;
  allocator_ = &allocator;

  std::lock_guard lock(lock_);
  monochrome_led_ = &monochrome_led;
  monochrome_led_->Enable().IgnoreError();
  TurnOff(*monochrome_led_);
}

Blinky::~Blinky() { blink_task_.Deregister(); }

void Blinky::Toggle() {
  blink_task_.Deregister();
  PW_LOG_INFO("Toggling LED");
  std::lock_guard lock(lock_);
  ToggleIo(*monochrome_led_);
}

void Blinky::SetLed(bool on) {
  blink_task_.Deregister();
  std::lock_guard lock(lock_);
  if (on) {
    PW_LOG_INFO("Setting LED on");
    TurnOn(*monochrome_led_);
  } else {
    PW_LOG_INFO("Setting LED off");
    TurnOff(*monochrome_led_);
  }
}

pw::Status Blinky::Blink(uint32_t blink_count, uint32_t interval_ms) {
  if (blink_count == 0) {
    PW_LOG_INFO("Blinking forever at a %ums interval", interval_ms);
  } else {
    PW_LOG_INFO("Blinking %u times at a %ums interval", blink_count,
                interval_ms);
  }

  pw::chrono::SystemClock::duration interval =
      pw::chrono::SystemClock::for_at_least(
          std::chrono::milliseconds(interval_ms));

  blink_task_.Deregister();
  CoroContext coro_cx(*allocator_);
  blink_task_.SetCoro(BlinkLoop(coro_cx, blink_count, interval));
  dispatcher_->Post(blink_task_);
  return OkStatus();
}

bool Blinky::IsIdle() const {
  std::lock_guard lock(lock_);
  return !blink_task_.IsRegistered();
}

}  // namespace demo
