load("//third_party/pigweed/platforms/rp2:binary.bzl", "define_rp2040_binary_rule", "define_rp2350_binary_rule")

_APP_FLAGS = {
    "//apps/sbr/system:system": "//apps/sbr/system:rp2_system",
}

rp2040_binary = define_rp2040_binary_rule(_APP_FLAGS)
rp2350_binary = define_rp2350_binary_rule(_APP_FLAGS)
