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

#include "examples/pigweed/modules/blinky/blinky.h"
#include "examples/pigweed/modules/blinky/blinky.rpc.pb.h"
#include "pw_allocator/allocator.h"
#include "pw_async2/dispatcher.h"

namespace demo {

class BlinkyService final
    : public ::blinky::pw_rpc::nanopb::Blinky::Service<BlinkyService> {
 public:
  void Init(pw::async2::Dispatcher& dispatcher, pw::Allocator& allocator,
            pw::digital_io::DigitalInOut& monochrome_led);

  pw::Status ToggleLed(const pw_protobuf_Empty&, pw_protobuf_Empty&);

  pw::Status SetLed(const blinky_SetLedRequest& request, pw_protobuf_Empty&);

  pw::Status Blink(const blinky_BlinkRequest& request, pw_protobuf_Empty&);

  pw::Status IsIdle(const pw_protobuf_Empty&,
                    blinky_BlinkIdleResponse& response);

 private:
  Blinky blinky_;
};

}  // namespace demo
