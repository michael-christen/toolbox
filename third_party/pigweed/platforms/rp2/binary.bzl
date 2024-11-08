"""Project-specific bazel transitions for rp2xxx-series chips.

TODO:  b/301334234 - Use platform-based flags and retire these transitions.

Originally sourced from https://pigweed.googlesource.com/pigweed/showcase/sense/ with modifications
"""

load("@pigweed//pw_build:merge_flags.bzl", "merge_flags_for_transition_impl", "merge_flags_for_transition_outputs")
load("@pigweed//targets/rp2040:transition.bzl", "RP2_SYSTEM_FLAGS")

_COMMON_FLAGS = merge_flags_for_transition_impl(
    base = RP2_SYSTEM_FLAGS,
    override = {
        "@freertos//:freertos_config": "//third_party/pigweed/platforms/rp2:freertos_config",
        "@pico-sdk//bazel/config:PICO_CLIB": "llvm_libc",
        "@pico-sdk//bazel/config:PICO_TOOLCHAIN": "clang",
        "@pigweed//pw_build:default_module_config": "//system:module_config",
        "@pigweed//pw_system:extra_platform_libs": "//third_party/pigweed/platforms/rp2:extra_platform_libs",
        "@pigweed//pw_system:io_backend": "@pigweed//pw_system:sys_io_target_io",
        "@pigweed//pw_toolchain:cortex-m_toolchain_kind": "clang",
        "@pigweed//pw_unit_test:config_override": "//third_party/pigweed/platforms/rp2:64k_unit_tests",
    },
)

_RP2040_FLAGS = {
    "//command_line_option:platforms": "//third_party/pigweed/platforms/rp2:rp2040",
}

_RP2350_FLAGS = {
    "//command_line_option:platforms": "//third_party/pigweed/platforms/rp2:rp2350",
}

def _rp2_transition(device_specific_flags, app_flags):
    total_flags = dict(device_specific_flags, **app_flags)

    def _rp2_transition_impl(settings, attr):
        # buildifier: disable=unused-variable
        _ignore = settings, attr
        return merge_flags_for_transition_impl(
            base = _COMMON_FLAGS,
            override = total_flags,
        )

    return transition(
        implementation = _rp2_transition_impl,
        inputs = [],
        outputs = merge_flags_for_transition_outputs(
            base = _COMMON_FLAGS,
            override = total_flags,
        ),
    )

def _rp2_binary_impl(ctx):
    out = ctx.actions.declare_file(ctx.label.name)
    ctx.actions.symlink(output = out, is_executable = True, target_file = ctx.executable.binary)
    return [DefaultInfo(files = depset([out]), executable = out)]


def define_rp2040_binary_rule(app_flags):
    return rule(
        _rp2_binary_impl,
        attrs = {
            "binary": attr.label(
                doc = "cc_binary to build for the rp2040",
                cfg = _rp2_transition(_RP2040_FLAGS, app_flags),
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

def define_rp2350_binary_rule(app_flags):
    return rule(
        _rp2_binary_impl,
        attrs = {
            "binary": attr.label(
                doc = "cc_binary to build for the rp2350",
                cfg = _rp2_transition(_RP2350_FLAGS, app_flags),
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
