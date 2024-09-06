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

#include "examples/pigweed/modules/timer_future/timer_future.h"

namespace demo {

using ::pw::async2::Context;
using ::pw::async2::Pending;
using ::pw::async2::Poll;
using ::pw::async2::Ready;
using ::pw::async2::WaitReason;
using ::pw::chrono::SystemClock;
using ::pw::chrono::SystemTimer;

AsyncTimer::AsyncTimer()
    : waker_(),
      deadline_(),
      timer_([this](SystemClock::time_point) { std::move(waker_).Wake(); }) {}

TimerFuture AsyncTimer::WaitUntil(SystemClock::time_point deadline) {
  timer_.Cancel();
  waker_.Clear();
  deadline_ = deadline;
  timer_.InvokeAt(deadline);
  return TimerFuture(*this);
}

TimerFuture AsyncTimer::WaitFor(SystemClock::duration duration) {
  return WaitUntil(SystemClock::now() + duration);
}

Poll<> TimerFuture::Pend(Context& cx) {
  async_timer_.waker_ = cx.GetWaker(WaitReason::Unspecified());
  if (SystemClock::now() < async_timer_.deadline_) {
    return Pending();
  }
  async_timer_.waker_.Clear();
  return Ready();
}

}  // namespace demo
