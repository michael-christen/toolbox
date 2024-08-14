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
#pragma once

#include "pw_async2/dispatcher.h"
#include "pw_chrono/system_clock.h"
#include "pw_chrono/system_timer.h"

namespace demo {

class TimerFuture;

class AsyncTimer {
 public:
  // AsyncTimer is not movable due to the timer keeping a reference to the
  // waker.
  AsyncTimer();
  AsyncTimer(const AsyncTimer&) = delete;
  AsyncTimer& operator=(const AsyncTimer&) = delete;
  AsyncTimer(AsyncTimer&&) = delete;
  AsyncTimer& operator=(AsyncTimer&&) = delete;
  ~AsyncTimer() { timer_.Cancel(); }

  TimerFuture WaitUntil(pw::chrono::SystemClock::time_point deadline);
  TimerFuture WaitFor(pw::chrono::SystemClock::duration duration);

 private:
  friend class TimerFuture;

  pw::async2::Waker waker_;
  pw::chrono::SystemClock::time_point deadline_;
  pw::chrono::SystemTimer timer_;
};

class TimerFuture {
 public:
  pw::async2::Poll<> Pend(pw::async2::Context& cx);

 private:
  friend class AsyncTimer;

  TimerFuture(AsyncTimer& async_timer) : async_timer_(async_timer) {}
  AsyncTimer& async_timer_;
};

}  // namespace demo