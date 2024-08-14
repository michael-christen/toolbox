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

load("@pigweed//pw_build:compatibility.bzl", "incompatible_with_mcu")

package(default_visibility = ["//visibility:public"])

cc_library(
    name = "system",
    srcs = [
        "led.cc",
        "system.cc",
    ],
    implementation_deps = [
        "@pigweed//pw_channel",
        "@pigweed//pw_channel:stream_channel",
        "@pigweed//pw_digital_io",
        "@pigweed//pw_digital_io:digital_io_mock",
        "@pigweed//pw_multibuf:simple_allocator",
        "@pigweed//pw_system:async",
        "@pigweed//pw_system:io",
    ],
    target_compatible_with = incompatible_with_mcu(),
    deps = ["//system:headers"],
)
