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

#include "pw_digital_io/digital_io.h"

// The functions in this file return specific implementations of singleton types
// provided by the system.

namespace demo::system {

/// Initializes the system. This must be called before anything else in `main`.
void Init();

/// Starts the main system scheduler. This function never returns.
[[noreturn]] void Start();

pw::digital_io::DigitalInOut& MonochromeLed();

}  // namespace demo::system

