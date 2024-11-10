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
#define PW_LOG_MODULE_NAME "MAIN"

#include "examples/pigweed/modules/blinky/service.h"
#include "examples/pigweed/system/system.h"
#include "pw_log/log.h"
#include "pw_system/system.h"

int main() {
  demo::system::Init();
  auto& rpc_server = pw::System().rpc_server();
  auto& monochrome_led = demo::system::MonochromeLed();

  static demo::BlinkyService blinky_service;
  blinky_service.Init(pw::System().dispatcher(), pw::System().allocator(),
                      monochrome_led);
  rpc_server.RegisterService(blinky_service);

  PW_LOG_INFO("Started blinky app; waiting for RPCs...");
  demo::system::Start();
  PW_UNREACHABLE;
}
