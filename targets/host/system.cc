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

#include <signal.h>
#include <stdio.h>

#include "pw_assert/check.h"
#include "pw_channel/stream_channel.h"
#include "pw_digital_io/digital_io.h"
#include "pw_multibuf/simple_allocator.h"
#include "pw_system/io.h"
#include "pw_system/system.h"
#include "pw_thread_stl/options.h"

using ::pw::channel::StreamChannel;
using ::pw::digital_io::DigitalIn;
using ::pw::digital_io::State;

extern "C" {

void CtrlCSignalHandler(int /* ignored */) {
  printf("\nCtrl-C received; simulator exiting immediately...\n");
  // Skipping the C++ destructors since we want to exit immediately.
  _exit(0);
}

}  // extern "C"

void InstallCtrlCSignalHandler() {
  // Catch Ctrl-C to force a 0 exit code (success) to avoid signaling an error
  // for intentional exits. For example, VSCode shows an alarming dialog on
  // non-zero exit, which is confusing for users intentionally quitting.
  signal(SIGINT, CtrlCSignalHandler);
}

namespace {
class VirtualInput : public DigitalIn {
 public:
  VirtualInput(State state) : state_(state) {}

 private:
  pw::Status DoEnable(bool) override { return pw::OkStatus(); }
  pw::Result<State> DoGetState() override { return state_; }

  State state_;
};

VirtualInput io_sw_a(State::kInactive);
VirtualInput io_sw_b(State::kInactive);
VirtualInput io_sw_x(State::kInactive);
VirtualInput io_sw_y(State::kInactive);

}  // namespace

namespace demo::system {

void Init() {}

void Start() {
  InstallCtrlCSignalHandler();
  printf("==========================================\n");
  printf("=== Pigweed Quickstart: Host Simulator ===\n");
  printf("==========================================\n");
  printf("Simulator is now running. To connect with a console,\n");
  printf("either run one in a new terminal:\n");
  printf("\n");
  printf("   $ bazelisk run //blinky:simulator_console\n");
  printf("\n");
  printf("one from VSCode under the 'Bazel Build Targets' explorer tab.\n");
  printf("\n");
  printf("Press Ctrl-C to exit\n");

  static std::byte channel_buffer[16384];
  static pw::multibuf::SimpleAllocator multibuf_alloc(channel_buffer,
                                                      pw::System().allocator());
  static pw::NoDestructor<StreamChannel> channel(multibuf_alloc,
                                                 pw::system::GetReader(),
                                                 pw::thread::stl::Options(),
                                                 pw::system::GetWriter(),
                                                 pw::thread::stl::Options());

  pw::SystemStart(*channel);
  PW_UNREACHABLE;
}

}  // namespace demo::system
