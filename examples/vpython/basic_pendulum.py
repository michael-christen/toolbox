import dataclasses
import math

import vpython



@dataclasses.dataclass
class Constants:
    l: float
    m1: float
    g: float
    friction: float


@dataclasses.dataclass
class State:
    theta_d0: float
    theta_d1: float


@dataclasses.dataclass
class Input:
    tau_0: float



def compute_derivative_state(
    constants: Constants,
    input_val: Input,
    state: State,
) -> State:
    """

    theta_d2 = g * sin(theta_d0) / l
    """
    return State(
        theta_d0=state.theta_d1,
        theta_d1=(constants.g / constants.l) * math.sin(state.theta_d0) -
        state.theta_d1 * constants.friction,
    )


def main() -> None:

    constants = Constants(
        l=1,
        m1=0.1,
        g=9.81,
        friction=0.0,
    )
    state = State(
        theta_d0=math.pi / 6,
        theta_d1=0,
    )
    input_val = Input(tau_0=0)

    plane = vpython.box(length=5, height=0.001, width=5)
    staff = vpython.cylinder(length=constants.l, height=0.1, width=0.1)
    staff.rotate(math.pi/2, axis=vpython.vec(0,0,1))
    staff.rotate(-state.theta_d0, axis=vpython.vec(0,0,1))

    graph = vpython.graph(title='Misc', xtitle='t', ytitle='Misc',
                              scroll=True, xmin=0, xmax=30,
                              )
    graph_theta_d0 = vpython.gcurve(color=vpython.color.red, label='theta_d0')
    graph_theta_d1 = vpython.gcurve(color=vpython.color.blue, label='theta_d1')
    graph_theta_d2 = vpython.gcurve(color=vpython.color.green, label='theta_d2')

    energy = vpython.graph(title='Energy', xtitle='t', ytitle='Energy (J)',
                              scroll=True, xmin=0, xmax=30,
                              )
    graph_potential = vpython.gcurve(color=vpython.color.red, label='potential')
    graph_kinetic = vpython.gcurve(color=vpython.color.blue, label='kinetic')
    graph_total = vpython.gcurve(color=vpython.color.green, label='total')

    dt = 1/(60)
    t = 0.0
    while True:
        vpython.rate(1/dt)

        d_state = compute_derivative_state(constants=constants,
                                           input_val=input_val,
                                           state=state)
        # XXX: Doing all at the same time is likely best (use same value, see
        # elsewhere)
        state.theta_d1 += d_state.theta_d1 * dt
        state.theta_d0 += state.theta_d1 * dt

        # Animate
        staff.rotate(angle=-d_state.theta_d0 * dt, axis=vpython.vec(0,0,1))

        potential_energy = (constants.m1 * constants.g *
                            math.cos(state.theta_d0) * constants.l)
        v = state.theta_d1 * constants.l
        kinetic_energy = constants.m1 * (v **2) / 2
        # XXX: Not growing unbounded anymore, but still oscillating ~ 0.02,
        # though it changes based on the dt used, so perhaps it's ok?
        # NOTE: This is not factoring in heat loss of friction, so if that's
        # non-zero, you'll see this dropping
        total_energy = potential_energy + kinetic_energy

        # Graph (XXX: Maybe before)
        graph_theta_d0.plot(t, state.theta_d0)
        graph_theta_d1.plot(t, state.theta_d1)
        graph_theta_d2.plot(t, d_state.theta_d1)

        graph_potential.plot(t, potential_energy)
        graph_kinetic.plot(t, kinetic_energy)
        graph_total.plot(t, total_energy)

        t += dt


if __name__ == '__main__':
    main()
