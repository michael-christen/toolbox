package(default_visibility = ["//visibility:public"])

# --------------------
# --- OS Platforms ---
# --------------------

platform(
    name = "freertos",
    constraint_values = [
        "@pigweed//pw_build/constraints/rtos:freertos",
        "@platforms//os:none",
    ],
)

platform(
    name = "embos",
    constraint_values = [
        "@pigweed//pw_build/constraints/rtos:embos",
        "@platforms//os:none",
    ],
)

platform(
    name = "threadx",
    constraint_values = [
        "@pigweed//pw_build/constraints/rtos:threadx",
        "@platforms//os:none",
    ],
)

# --------------------------
# --- Hardware Platforms ---
# --------------------------
platform(
    name = "lm3s6965evb",
    constraint_values = [
        "@pw_toolchain//constraints/arm_mcpu:cortex-m3",
        "@pigweed//pw_build/constraints/chipset:lm3s6965evb",
        "@platforms//cpu:armv7-m",
        "@platforms//os:none",
        "@rust_crates//:no_std",
    ],
)

platform(
    name = "nrf52833",
    constraint_values = [
        "@pw_toolchain//constraints/arm_mcpu:cortex-m0",
        "@pigweed//pw_build/constraints/chipset:nrf52833",
        "@platforms//cpu:armv6-m",
        "@platforms//os:none",
    ],
)

# Primarily a QEMU supported m0 target for rust development, based on the
# nRF51822.
platform(
    name = "microbit",
    constraint_values = [
        "@pigweed//pw_build/constraints/board:microbit",
        "@rust_crates//:no_std",
        "@platforms//os:none",
        # We have no pw_sys_io backend for this platform.
    ],
    parents = [":nrf52833"],
)

# ----------------------
# --- Misc Platforms ---
# ----------------------

platform(
    name = "none",
    constraint_values = ["@platforms//os:none"],
)
