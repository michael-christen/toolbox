import math

import vpython

"""

- [ ] Spin wheels
- [ ] Control orientation of body
- [ ] add key input
"""


def main() -> None:
    body = vpython.box(length=5, height=10, width=2, color=vpython.color.orange)
    WHEEL_RADIUS = 2
    WHEEL_WIDTH = 0.5
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


    def key_pressed(evt):  # info about event is stored in evt
        WHEEL_ANGLE_PER_DT = 5 * (math.pi / 180)
        BODY_ANGLE_PER_DT = math.pi / 180
        if isinstance(evt, str):
            keyname = evt
        else:
            keyname = evt.key
        if keyname == 'k':
            r_wheel_assembly.rotate(angle=WHEEL_ANGLE_PER_DT)
        elif keyname == 'j':
            r_wheel_assembly.rotate(angle=-WHEEL_ANGLE_PER_DT)
        elif keyname == 'd':
            l_wheel_assembly.rotate(angle=WHEEL_ANGLE_PER_DT)
        elif keyname == 'f':
            l_wheel_assembly.rotate(angle=-WHEEL_ANGLE_PER_DT)
        elif keyname == 'up':
            body.rotate(angle=BODY_ANGLE_PER_DT, origin=r_wheel.pos)
        elif keyname == 'down':
            body.rotate(angle=-BODY_ANGLE_PER_DT, origin=r_wheel.pos)

    # XXX: Make the plane actually a set of curves
    vpython.scene.bind('keydown', key_pressed)

    while True:
        vpython.rate(60)
        keys_down = vpython.keysdown()
        for k in keys_down:
            key_pressed(k)


if __name__ == '__main__':
    main()
