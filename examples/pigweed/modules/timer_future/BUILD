# Copyright 2024 The Pigweed Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

package(default_visibility = ["//visibility:private"])

cc_library(
    name = "timer_future",
    srcs = ["timer_future.cc"],
    hdrs = ["timer_future.h"],
    visibility = ["//visibility:public"],
    deps = [
        "@pigweed//pw_async2:dispatcher",
        "@pigweed//pw_chrono:system_clock",
        "@pigweed//pw_chrono:system_timer",
    ],
)
