import dataclasses
import math

import vpython

"""

- [ ] Spin wheels
- [ ] Control orientation of body
- [ ] add key input
"""

# XXX: suffix fields with units?


@dataclasses.dataclass
class DriveConstants:
    axis_length: float
    wheel_radius: float


@dataclasses.dataclass
class DriveState:
    x: float
    y: float
    angle: float


@dataclasses.dataclass
class DriveInput:
    right_wheel_angular_rate: float
    left_wheel_angular_rate: float


def compute_derivative_state(
    drive_constants: DriveConstants,
    drive_input: DriveInput,
    drive_state: DriveState,
) -> DriveState:
    R = drive_constants.wheel_radius
    L = drive_constants.axis_length
    phi_r = drive_input.right_wheel_angular_rate
    phi_l = drive_input.left_wheel_angular_rate

    v_x = R / 2 * (phi_r + phi_l)
    omega = R / L * (phi_r - phi_l)
    # We provide this in "world" coordinates
    return DriveState(
        x=v_x * math.cos(drive_state.angle),
        y=v_x * math.sin(drive_state.angle),
        angle=omega,
    )


def main() -> None:
    vpython.scene.visible = False
    my_scene = vpython.canvas(width=1_000, height=1_000)  # noqa: F841

    graph_pos = vpython.graph(  # noqa: F841
        title="Positions",
        xtitle="t",
        ytitle="position",
        scroll=True,
        xmin=0,
        xmax=30,
    )
    graph_x = vpython.gcurve(color=vpython.color.red, label="x")
    graph_y = vpython.gcurve(color=vpython.color.blue, label="y")

    graph_angle = vpython.graph(  # noqa: F841
        title="Angle",
        xtitle="t",
        ytitle="angle",
        scroll=True,
        xmin=0,
        xmax=30,
    )
    graph_angle_curve = vpython.gcurve(color=vpython.color.red, label="θ")

    body = vpython.box(
        length=5, height=10, width=2, color=vpython.color.orange
    )
    WHEEL_RADIUS = 2
    WHEEL_WIDTH = 0.5
    DRIVE_CONSTANTS = DriveConstants(
        axis_length=body.length + (WHEEL_WIDTH / 2) * 2,
        wheel_radius=WHEEL_RADIUS,
    )
    r_wheel = vpython.cylinder(
        pos=vpython.vec(-body.length / 2, -body.height / 2, 0),
        axis=vpython.vec(-WHEEL_WIDTH, 0, 0),
        # starboard = right = green
        color=vpython.color.green,
        radius=WHEEL_RADIUS,
        # Failing to see texture
        # texure=vpython.textures.stucco,
    )
    l_wheel = vpython.cylinder(
        pos=vpython.vec(body.length / 2, -body.height / 2, 0),
        axis=vpython.vec(WHEEL_WIDTH, 0, 0),
        # port = left = red
        radius=WHEEL_RADIUS,
        color=vpython.color.red,
        # texure=vpython.textures.stucco,
    )
    # XXX: We can't rotate parts of a compound after they are bound together
    vehicle = vpython.compound(
        [l_wheel, r_wheel, body],
        make_trail=True,
        origin=vpython.vec(0, -(body.height / 2), 0),
        # trail_type="points",
        # retain=1000,
    )
    myarrow = vpython.attach_arrow(
        vehicle, "axis", scale=1.0, shaftwidth=0.2
    )  # noqa: F841

    # XXX: Make the plane actually a set of curves
    PLANE_HEIGHT = 0.5
    plane = vpython.box(  # noqa: F841
        pos=(
            vpython.vec(
                0, -(body.height / 2 + WHEEL_RADIUS) - PLANE_HEIGHT / 2, 0
            )
        ),
        length=10,
        height=-PLANE_HEIGHT,
        width=10,
        color=vpython.color.gray(0.95),
    )

    drive_state = DriveState(
        x=0,
        y=0,
        angle=0,
    )
    drive_input = DriveInput(
        right_wheel_angular_rate=0,
        left_wheel_angular_rate=0,
    )

    dt = 1 / 60.0
    t = 0

    def key_pressed(evt):  # info about event is stored in evt
        WHEEL_ANGLE_PER_DT = 360 * (math.pi / 180)
        BODY_ANGLE_PER_DT = math.pi / 180
        if isinstance(evt, str):
            keyname = evt
        else:
            keyname = evt.key
        if keyname == "k":
            drive_input.right_wheel_angular_rate = WHEEL_ANGLE_PER_DT
        elif keyname == "j":
            drive_input.right_wheel_angular_rate = -WHEEL_ANGLE_PER_DT
        elif keyname == "d":
            drive_input.left_wheel_angular_rate = WHEEL_ANGLE_PER_DT
        elif keyname == "f":
            drive_input.left_wheel_angular_rate = -WHEEL_ANGLE_PER_DT
        elif keyname == "up":
            vehicle.rotate(angle=BODY_ANGLE_PER_DT)
        elif keyname == "down":
            vehicle.rotate(angle=-BODY_ANGLE_PER_DT)

    # vpython.scene.bind('keydown', key_pressed)

    while True:
        vpython.rate(1 / dt)

        # Control
        drive_input.right_wheel_angular_rate = 0
        drive_input.left_wheel_angular_rate = 0
        keys_down = vpython.keysdown()
        for k in keys_down:
            key_pressed(k)

        # Compute and integrate
        drive_change = compute_derivative_state(
            drive_constants=DRIVE_CONSTANTS,
            drive_input=drive_input,
            drive_state=drive_state,
        )
        drive_state.x += drive_change.x * dt
        drive_state.y += drive_change.y * dt
        drive_state.angle += drive_change.angle * dt

        # Apply to animation
        # XXX: Could be nice to set this explicitly
        vehicle.rotate(
            axis=vpython.vec(0, 1, 0), angle=drive_change.angle * dt
        )
        # x, y, z: in our context it's y, z, x
        vehicle.pos = vpython.vec(
            drive_state.y, -body.height / 2, drive_state.x
        )

        # Graph
        graph_x.plot(t, drive_state.x)
        graph_y.plot(t, drive_state.y)
        graph_angle_curve.plot(t, drive_state.angle)

        # Step
        t += dt


if __name__ == "__main__":
    main()
