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
# From https://pigweed.googlesource.com/pigweed/showcase/sense/

load("//bzl:cc.bzl", "cc_library")

package(default_visibility = ["//visibility:public"])

# This is an incomplete platform, do NOT try to pass this
# as a --platforms flag value. Use :rp2040 or :rp2350.
platform(
    name = "rp2_common",
    constraint_values = [
        "@freertos//:disable_task_statics",
        "@pigweed//pw_build/constraints/rtos:freertos",
        "@pigweed//pw_build/constraints/chipset:rp2040",  # TODO: https://pwbug.dev/343487589 - Use Pico SDK constraints.
        "@pigweed//pw_cpu_exception:enabled",
        "@pigweed//pw_interrupt_cortex_m:backend",
        "@platforms//os:none",
    ],
)

platform(
    name = "rp2040",
    constraint_values = [
        "@freertos//:port_ARM_CM0",
        "@pico-sdk//bazel/constraint:rp2040",
        # For toolchain selection.
        "@platforms//cpu:armv6-m",
        "@pigweed//pw_build/constraints/arm:cortex-m0",
    ],
    parents = [":rp2_common"],
)

platform(
    name = "rp2350",
    constraint_values = [
        "@freertos//:port_ARM_CM33_NTZ",
        "@pico-sdk//bazel/constraint:rp2350",
        # For toolchain selection.
        "@platforms//cpu:armv8-m",
        "@pigweed//pw_build/constraints/arm:cortex-m33",
    ],
    parents = [":rp2_common"],
)

cc_library(
    name = "extra_platform_libs",
    deps = [
        "@pico-sdk//src/rp2_common/pico_stdlib:pico_stdlib",
        "@pigweed//pw_tokenizer:linker_script",
    ] + select({
        "@rules_cc//cc/compiler:clang": [
            "@pigweed//pw_libcxx",
        ],
        "//conditions:default": [],
    }),
    alwayslink = 1,
)

cc_library(
    name = "freertos_config",
    hdrs = [
        "config/FreeRTOSConfig.h",
    ],
    includes = ["config"],
    deps = ["@pigweed//third_party/freertos:config_assert"],
)

cc_library(
    name = "thread_config_overrides",
    defines = [
        "PW_THREAD_FREERTOS_CONFIG_JOINING_ENABLED=1",
    ],
)
