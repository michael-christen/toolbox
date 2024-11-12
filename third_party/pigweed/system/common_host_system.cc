#include "third_party/pigweed/system/common_host_system.h"

#include <signal.h>
#include <stdio.h>

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

namespace third_party {
namespace pigweed {
namespace system {
namespace internal {

void CommonHostStartSetup(const char* bazel_console_path) {
  InstallCtrlCSignalHandler();
  printf("==========================================\n");
  printf("=== Pigweed Quickstart: Host Simulator ===\n");
  printf("==========================================\n");
  printf("Simulator is now running. To connect with a console,\n");
  printf("either run one in a new terminal:\n");
  printf("\n");
  printf("   $ bazel run %s\n", bazel_console_path);
  printf("\n");
  printf("one from VSCode under the 'Bazel Build Targets' explorer tab.\n");
  printf("\n");
  printf("Press Ctrl-C to exit\n");
}

}

}  // namespace system
}  // namespace sbr
}  // namespace apps
