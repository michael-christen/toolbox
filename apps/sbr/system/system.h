#pragma once

// The functions in this file return specific implementations of singleton types
// provided by the system.

namespace apps {
namespace sbr {
namespace system {

/// Initializes the system. This must be called before anything else in `main`.
void Init();

/// Starts the main system scheduler. This function never returns.
[[noreturn]] void Start();

}  // namespace system
}  // namespace sbr
}  // namespace apps
