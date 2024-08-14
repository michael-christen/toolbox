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

"""Project-specific bazel transitions for rp2xxx-series chips.

TODO:  b/301334234 - Use platform-based flags and retire these transitions.
"""

load("@pigweed//pw_build:merge_flags.bzl", "merge_flags_for_transition_impl", "merge_flags_for_transition_outputs")
load("@pigweed//targets/rp2040:transition.bzl", "RP2_SYSTEM_FLAGS")

_COMMON_FLAGS = merge_flags_for_transition_impl(
    base = RP2_SYSTEM_FLAGS,
    override = {
        "//system:system": "//targets/rp2:system",
        "@freertos//:freertos_config": "//targets/rp2:freertos_config",
        "@pico-sdk//bazel/config:PICO_CLIB": "llvm_libc",
        "@pico-sdk//bazel/config:PICO_TOOLCHAIN": "clang",
        "@pigweed//pw_build:default_module_config": "//system:module_config",
        "@pigweed//pw_system:extra_platform_libs": "//targets/rp2:extra_platform_libs",
        "@pigweed//pw_system:io_backend": "@pigweed//pw_system:sys_io_target_io",
        "@pigweed//pw_toolchain:cortex-m_toolchain_kind": "clang",
        "@pigweed//pw_unit_test:config_override": "//targets/rp2:64k_unit_tests",
    },
)

_RP2040_FLAGS = {
    "//command_line_option:platforms": "//targets/rp2:rp2040",
}

_RP2350_FLAGS = {
    "//command_line_option:platforms": "//targets/rp2:rp2350",
}

def _rp2_transition(device_specific_flags):
    def _rp2_transition_impl(settings, attr):
        # buildifier: disable=unused-variable
        _ignore = settings, attr
        return merge_flags_for_transition_impl(
            base = _COMMON_FLAGS,
            override = device_specific_flags,
        )

    return transition(
        implementation = _rp2_transition_impl,
        inputs = [],
        outputs = merge_flags_for_transition_outputs(
            base = _COMMON_FLAGS,
            override = device_specific_flags,
        ),
    )

def _rp2_binary_impl(ctx):
    out = ctx.actions.declare_file(ctx.label.name)
    ctx.actions.symlink(output = out, is_executable = True, target_file = ctx.executable.binary)
    return [DefaultInfo(files = depset([out]), executable = out)]

rp2040_binary = rule(
    _rp2_binary_impl,
    attrs = {
        "binary": attr.label(
            doc = "cc_binary to build for the rp2040",
            cfg = _rp2_transition(_RP2040_FLAGS),
            executable = True,
            mandatory = True,
        ),
        "_allowlist_function_transition": attr.label(
            default = "@bazel_tools//tools/allowlists/function_transition_allowlist",
        ),
    },
    doc = "Builds the specified binary for the rp2040 platform",
    # This target is for rp2040 and can't be run on host.
    executable = False,
)

rp2350_binary = rule(
    _rp2_binary_impl,
    attrs = {
        "binary": attr.label(
            doc = "cc_binary to build for the rp2040",
            cfg = _rp2_transition(_RP2350_FLAGS),
            executable = True,
            mandatory = True,
        ),
        "_allowlist_function_transition": attr.label(
            default = "@bazel_tools//tools/allowlists/function_transition_allowlist",
        ),
    },
    doc = "Builds the specified binary for the rp2350 platform",
    # This target is for rp2350 and can't be run on host.
    executable = False,
)
