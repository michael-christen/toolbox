#include <signal.h>
#include <stdio.h>

#include "apps/sbr/system/system.h"
#include "platforms/host/initiator_host.h"
#include "pw_assert/check.h"
#include "pw_channel/stream_channel.h"
#include "pw_digital_io/digital_io.h"
#include "pw_i2c/address.h"
#include "pw_multibuf/simple_allocator.h"
#include "pw_system/io.h"
#include "pw_system/system.h"
#include "pw_thread_stl/options.h"

using ::pw::channel::StreamChannel;

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

namespace apps {
namespace sbr {
namespace system {

void Init() {}

void Start() {
  InstallCtrlCSignalHandler();
  printf("==========================================\n");
  printf("=== Pigweed Quickstart: Host Simulator ===\n");
  printf("==========================================\n");
  printf("Simulator is now running. To connect with a console,\n");
  printf("either run one in a new terminal:\n");
  printf("\n");
  printf("   $ bazel run //apps/sbr:simulator_console\n");
  printf("\n");
  printf("one from VSCode under the 'Bazel Build Targets' explorer tab.\n");
  printf("\n");
  printf("Press Ctrl-C to exit\n");

  static std::byte channel_buffer[16384];
  static pw::multibuf::SimpleAllocator multibuf_alloc(channel_buffer,
                                                      pw::System().allocator());
  static pw::NoDestructor<StreamChannel> channel(
      multibuf_alloc, pw::system::GetReader(), pw::thread::stl::Options(),
      pw::system::GetWriter(), pw::thread::stl::Options());

  pw::SystemStart(*channel);
  PW_UNREACHABLE;
}

pw::i2c::RegisterDevice& LIS3MDLRegisterDevice() {
  constexpr pw::i2c::Address kAddress = pw::i2c::Address::SevenBit<0x01>();

  static platforms::host::HostInitiator initiator;
  static pw::i2c::RegisterDevice reg_device(
      initiator, kAddress, cpp20::endian::little,
      pw::i2c::RegisterAddressSize::k1Byte);
  return reg_device;
}

}  // namespace system
}  // namespace sbr
}  // namespace apps
