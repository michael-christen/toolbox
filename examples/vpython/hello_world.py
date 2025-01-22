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


def compute_derivative_state(drive_constants: DriveConstants,
                             drive_input: DriveInput,
                             drive_state: DriveState) -> DriveState:
    R = drive_constants.wheel_radius
    L = drive_constants.axis_length
    phi_r = drive_input.right_wheel_angular_rate
    phi_l = drive_input.left_wheel_angular_rate

    v_x = R/2 * (phi_r + phi_l)
    omega = R/L * (phi_r - phi_l)
    # We provide this in "world" coordinates
    return DriveState(
        x=v_x * math.cos(drive_state.angle),
        y=v_x * math.sin(drive_state.angle),
        angle=omega,
    )


def main() -> None:
    vpython.scene.visible = False
    my_scene = vpython.canvas(width=1_000, height=1_000)

    body = vpython.box(length=5, height=10, width=2, color=vpython.color.orange)
    WHEEL_RADIUS = 2
    WHEEL_WIDTH = 0.5
    DRIVE_CONSTANTS = DriveConstants(
        axis_length=body.length + (WHEEL_WIDTH/2)*2,
        wheel_radius=WHEEL_RADIUS,
    )
    r_wheel = vpython.cylinder(
        pos=vpython.vec(-body.length/2,-body.height/2,0),
        axis=vpython.vec(-WHEEL_WIDTH,0,0),
        # starboard = right = green
        color=vpython.color.green,
        radius=WHEEL_RADIUS,
        # Failing to see texture
        # texure=vpython.textures.stucco,
        )
    r_wheel_hub = vpython.box(length=-(WHEEL_WIDTH + 0.1), height=WHEEL_RADIUS,
                              width=WHEEL_RADIUS,
                              pos = r_wheel.pos - vpython.vec(WHEEL_WIDTH/2, 0,
                                                              0))
    r_wheel_assembly = vpython.compound([r_wheel, r_wheel_hub])
    l_wheel = vpython.cylinder(
        pos=vpython.vec(body.length/2,-body.height/2,0),
        axis=vpython.vec(WHEEL_WIDTH,0,0),
        # port = left = red
        radius=WHEEL_RADIUS,
        color=vpython.color.red,
        # texure=vpython.textures.stucco,
        )
    l_wheel_hub = vpython.box(length=WHEEL_WIDTH + 0.1, height=WHEEL_RADIUS,
                              width=WHEEL_RADIUS,
                              pos = l_wheel.pos + vpython.vec(WHEEL_WIDTH/2, 0,
                                                              0))
    l_wheel_assembly = vpython.compound([l_wheel, l_wheel_hub])
    wheels = [
        l_wheel_assembly,
        r_wheel_assembly,
    ]
    PLANE_HEIGHT = 0.5
    plane = vpython.box(
                        pos=(vpython.vec(0, -(body.height/2 + WHEEL_RADIUS) - PLANE_HEIGHT/2, 0)),
                        length=10, height=-PLANE_HEIGHT, width=10,
                        color=vpython.color.gray(0.95))
    vehicle = vpython.compound(wheels + [body], make_trail=True,
                               # trail_type="points",
                               # retain=1000,
                               )
    # myarrow = vpython.attach_arrow(vehicle, "velocity", scale=2.0)

    drive_state = DriveState(
        x=0,
        y=0,
        angle=0,
    )
    drive_input = DriveInput(
        right_wheel_angular_rate=0,
        left_wheel_angular_rate=0,
    )


    def key_pressed(evt):  # info about event is stored in evt
        WHEEL_ANGLE_PER_DT = 360 * (math.pi / 180)
        BODY_ANGLE_PER_DT = math.pi / 180
        if isinstance(evt, str):
            keyname = evt
        else:
            keyname = evt.key
        if keyname == 'k':
            # r_wheel_assembly.rotate(angle=WHEEL_ANGLE_PER_DT)
            drive_input.right_wheel_angular_rate = WHEEL_ANGLE_PER_DT
        elif keyname == 'j':
            # r_wheel_assembly.rotate(angle=-WHEEL_ANGLE_PER_DT)
            drive_input.right_wheel_angular_rate = -WHEEL_ANGLE_PER_DT
        elif keyname == 'd':
            # l_wheel_assembly.rotate(angle=WHEEL_ANGLE_PER_DT)
            drive_input.left_wheel_angular_rate = WHEEL_ANGLE_PER_DT
        elif keyname == 'f':
            # XXX: The assembly doesn't seem to rotate anymore after being
            # joined to a larger vehicle compound
            # l_wheel_assembly.rotate(angle=-WHEEL_ANGLE_PER_DT)
            drive_input.left_wheel_angular_rate = -WHEEL_ANGLE_PER_DT
        elif keyname == 'up':
            body.rotate(angle=BODY_ANGLE_PER_DT, origin=r_wheel.pos)
        elif keyname == 'down':
            body.rotate(angle=-BODY_ANGLE_PER_DT, origin=r_wheel.pos)
        elif keyname == 'left':
            vehicle.rotate(axis=vpython.vec(0,1,0), angle=BODY_ANGLE_PER_DT)
        elif keyname == 'right':
            vehicle.rotate(axis=vpython.vec(0,1,0), angle=-BODY_ANGLE_PER_DT)

    # XXX: Make the plane actually a set of curves
    vpython.scene.bind('keydown', key_pressed)

    dt = 1/60.0
    t = 0

    graph_pos = vpython.graph(title='Positions', xtitle='t', ytitle='position',
                              scroll=True, xmin=0, xmax=30,
                              )
    graph_x = vpython.gcurve(color=vpython.color.red, label='x')
    graph_y = vpython.gcurve(color=vpython.color.blue, label='y')

    graph_angle = vpython.graph(title='Angle', xtitle='t', ytitle='angle',
                                scroll=True, xmin=0, xmax=30,
                                )
    graph_angle_curve = vpython.gcurve(color=vpython.color.red, label='angle')

    while True:
        vpython.rate(1/dt)

        graph_x.plot(t, drive_state.x)
        graph_y.plot(t, drive_state.y)
        # Sim was growing quicker, forgot to multiply by dt

        graph_angle_curve.plot(t, drive_state.angle)


        keys_down = vpython.keysdown()
        for k in keys_down:
            key_pressed(k)
        if not keys_down:
            drive_input.right_wheel_angular_rate = 0
            drive_input.left_wheel_angular_rate = 0

        # Compute and integrate
        drive_change = compute_derivative_state(
            drive_constants=DRIVE_CONSTANTS,
            drive_input=drive_input,
            drive_state=drive_state)
        drive_state.x += drive_change.x * dt
        drive_state.y += drive_change.y * dt
        drive_state.angle += drive_change.angle * dt


        # Apply to animation
        # XXX: y, z, x
        vehicle.rotate(axis=vpython.vec(0,1,0), angle=drive_change.angle*dt)
        # XXX(next): our position doesn't quite seem to be updating properly
        # x, y, z: in our context it's y, z, x
        vehicle.pos += vpython.vec(drive_change.y*dt, 0, drive_change.x*dt)

        t += dt


if __name__ == '__main__':
    main()
