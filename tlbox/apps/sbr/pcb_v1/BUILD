load("//bzl:kicad.bzl", "kicad_drc", "kicad_gerbers", "kicad_pcb_svg", "kicad_schematic_pdf", "kicad_schematic_svgs")

package(default_visibility = ["//visibility:private"])

_SCHEMATIC_SRCS = [
    "self_balancing_robot_v1.kicad_sch",
    "imu.kicad_sch",
    "inner_piece.kicad_sch",
    "processor.kicad_sch",
    "pwm_controller.kicad_sch",
    "stepper_motor.kicad_sch",
    "uart_radio.kicad_sch",
]

kicad_schematic_svgs(
    name = "schematic_svgs",
    srcs = _SCHEMATIC_SRCS,
    top = "self_balancing_robot_v1.kicad_sch",
    visibility = ["//docs:__pkg__"],
)

kicad_schematic_pdf(
    name = "schematic_pdf",
    srcs = _SCHEMATIC_SRCS,
    top = "self_balancing_robot_v1.kicad_sch",
    visibility = ["//docs:__pkg__"],
)

kicad_pcb_svg(
    name = "pcb_svg",
    src = "self_balancing_robot_v1.kicad_pcb",
    visibility = ["//docs:__pkg__"],
)

kicad_gerbers(
    name = "gerbers",
    src = "self_balancing_robot_v1.kicad_pcb",
)

kicad_drc(
    name = "drc",
    src = "self_balancing_robot_v1.kicad_pcb",
)
