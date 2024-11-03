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

#include "apps/production/threads.h"
#include "pw_thread_freertos/context.h"
#include "pw_thread_freertos/options.h"

namespace sense {

pw::thread::freertos::StaticContextWithStack<1024> sensor_thread_context;

const pw::thread::Options& SamplingThreadOptions() {
  static constexpr auto kOptions =
      pw::thread::freertos::Options()
          .set_name("SensorThread")
          .set_static_context(sensor_thread_context)
          .set_priority(tskIDLE_PRIORITY + 1);
  return kOptions;
}

}  // namespace sense
