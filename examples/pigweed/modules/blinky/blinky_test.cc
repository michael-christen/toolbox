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

#include "examples/pigweed/modules/blinky/blinky.h"

#include "pw_allocator/testing.h"
#include "pw_async2/dispatcher_for_test.h"
#include "pw_async2/simulated_time_provider.h"
#include "pw_digital_io/digital_io_mock.h"
#include "pw_unit_test/framework.h"

namespace demo {

using AllocatorForTest = ::pw::allocator::test::AllocatorForTest<512>;
using ::pw::async2::DispatcherForTest;

// Test fixtures.

class BlinkyTest : public ::testing::Test {
 protected:
  using Event = ::pw::digital_io::DigitalInOutMockImpl::Event;
  using State = ::pw::digital_io::State;

  static constexpr uint32_t kIntervalMs = 10;
  static constexpr pw::chrono::SystemClock::duration kInterval =
      pw::chrono::SystemClock::for_at_least(
          std::chrono::milliseconds(kIntervalMs));

  BlinkyTest() : monochrome_led_(time_) {
    blinky_.Init(dispatcher_, time_, allocator_, monochrome_led_);
  }

  pw::InlineDeque<Event>::iterator FirstActive() {
    pw::InlineDeque<Event>& events = monochrome_led_.events();
    pw::InlineDeque<Event>::iterator event = events.begin();
    while (event != events.end()) {
      if (event->state == State::kActive) {
        break;
      }
      ++event;
    }
    return event;
  }

  uint32_t ToMs(pw::chrono::SystemClock::duration interval) {
    return std::chrono::duration_cast<std::chrono::milliseconds>(interval)
        .count();
  }

  static constexpr const size_t kEventCapacity = 256;

  AllocatorForTest allocator_;
  DispatcherForTest dispatcher_;
  pw::async2::SimulatedTimeProvider<pw::chrono::SystemClock> time_;
  pw::digital_io::DigitalInOutMock<kEventCapacity> monochrome_led_;
  Blinky blinky_;
};

// Unit tests.

// XXX: Test is failing, re-evaluate
TEST_F(BlinkyTest, Toggle) {
  auto start = time_.now();
  blinky_.Toggle();
  time_.AdvanceTime(kInterval * 1);
  blinky_.Toggle();
  time_.AdvanceTime(kInterval * 2);
  blinky_.Toggle();
  time_.AdvanceTime(kInterval * 3);
  blinky_.Toggle();

  auto event = FirstActive();
  ASSERT_NE(event, monochrome_led_.events().end());
  EXPECT_EQ(event->state, State::kActive);
  EXPECT_GE(ToMs(event->timestamp - start), kIntervalMs * 0);
  start = event->timestamp;

  ASSERT_NE(++event, monochrome_led_.events().end());
  EXPECT_EQ(event->state, State::kInactive);
  EXPECT_GE(ToMs(event->timestamp - start), kIntervalMs * 1);
  start = event->timestamp;

  ASSERT_NE(++event, monochrome_led_.events().end());
  EXPECT_EQ(event->state, State::kActive);
  EXPECT_GE(ToMs(event->timestamp - start), kIntervalMs * 2);
  start = event->timestamp;

  ASSERT_NE(++event, monochrome_led_.events().end());
  EXPECT_EQ(event->state, State::kInactive);
  EXPECT_GE(ToMs(event->timestamp - start), kIntervalMs * 3);
}

TEST_F(BlinkyTest, Blink) {
  auto start = time_.now();
  EXPECT_EQ(blinky_.Blink(1, kIntervalMs), pw::OkStatus());
  while (!blinky_.IsIdle()) {
    dispatcher_.RunUntilStalled();
    time_.AdvanceUntilNextExpiration();
  }

  auto event = FirstActive();
  ASSERT_NE(event, monochrome_led_.events().end());
  EXPECT_EQ(event->state, State::kActive);
  EXPECT_GE(ToMs(event->timestamp - start), kIntervalMs);
  start = event->timestamp;

  ASSERT_NE(++event, monochrome_led_.events().end());
  EXPECT_EQ(event->state, State::kInactive);
  EXPECT_GE(ToMs(event->timestamp - start), kIntervalMs);
}

TEST_F(BlinkyTest, BlinkMany) {
  auto start = time_.now();
  EXPECT_EQ(blinky_.Blink(100, kIntervalMs), pw::OkStatus());
  while (!blinky_.IsIdle()) {
    dispatcher_.RunUntilStalled();
    time_.AdvanceUntilNextExpiration();
  }

  // Every "on" and "off" is recorded.
  EXPECT_GE(monochrome_led_.events().size(), 200);
  EXPECT_GE(ToMs(time_.now() - start), kIntervalMs * 200);
}

TEST_F(BlinkyTest, BlinkSlow) {
  auto start = time_.now();
  EXPECT_EQ(blinky_.Blink(1, kIntervalMs * 32), pw::OkStatus());
  while (!blinky_.IsIdle()) {
    dispatcher_.RunUntilStalled();
    time_.AdvanceUntilNextExpiration();
  }

  auto event = FirstActive();
  ASSERT_NE(event, monochrome_led_.events().end());
  EXPECT_EQ(event->state, State::kActive);
  EXPECT_GE(ToMs(event->timestamp - start), kIntervalMs * 32);
  start = event->timestamp;

  ASSERT_NE(++event, monochrome_led_.events().end());
  EXPECT_EQ(event->state, State::kInactive);
  EXPECT_GE(ToMs(event->timestamp - start), kIntervalMs * 32);
}

}  // namespace demo
