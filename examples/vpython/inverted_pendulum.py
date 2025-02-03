import dataclasses

import numpy as np
import vpython


@dataclasses.dataclass
class Constants:
    i_w: float
    m_w: float
    m: float
    r: float
    l: float
    i: float
    # Roller damping ratio N*m / (rad / s)
    b_r: float
    # Bearing damping ratio
    b_m: float
    g: float


@dataclasses.dataclass
class Input:
    tau_0: float


@dataclasses.dataclass
class State:
    phi_d0: float
    theta_d0: float
    phi_d1: float
    theta_d1: float


def compute_derivative_state(
    constants: Constants,
    input_val: Input,
    state: State,
) -> State:
    """

    d/dt(x) = Ax + B 𝜏₀

    """

    c = constants

    # Linearized forms; keep theta small
    E = np.matrix(
        [
            [c.i_w + (c.m_w + c.m) * (c.r**2), c.m * c.r * c.l],
            [c.m * c.r * c.l, c.i + c.m * (c.l**2)],
        ]
    )
    F = np.matrix(
        [
            [c.b_r + c.b_m, -c.b_m],
            [-c.b_m, c.b_m],
        ]
    )
    G = np.matrix(
        [
            [0],
            [-c.m * c.g * c.l],
        ]
    )
    H = np.matrix(
        [
            [1],
            [-1],
        ]
    )
    n_i_E = -np.linalg.inv(E)

    _A_top = np.matrix(
        [
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    _A_bot = np.hstack(
        [
            np.matrix([[0], [0]]),
            n_i_E * G,
            n_i_E * F,
        ]
    )
    A = np.vstack([_A_top, _A_bot])

    B = np.vstack([np.matrix([[0], [0]]), n_i_E * H])
    # XXX: Could optimize by pre-computing ^

    x = np.matrix(
        [
            [state.phi_d0],
            [state.theta_d0],
            [state.phi_d1],
            [state.theta_d1],
        ]
    )

    result = A * x + B * input_val.tau_0
    return State(
        phi_d0=result[0, 0],
        theta_d0=result[1, 0],
        phi_d1=result[2, 0],
        theta_d1=result[3, 0],
    )


l1 = 40e-3  # meter
l2 = 60e-3


def get_constants() -> Constants:
    m = 513.3e-3  # kg
    # XXX: Was 0 earlier
    m2 = 50e-3
    m1 = m - m2
    # XXX: Why 12?
    i = m1 * (l1 / 2 + l2) ** 2 + m2 * l2 * l2 / 12
    # position of center of mass
    length = l2 / 2 + (l1 + l2) * m1 / (2 * m)
    return Constants(
        # XXX: Why x 2?
        i_w=389.6e-9 * 2,
        m_w=7.2e-3,
        m=m,
        r=16e-3,
        l=length,
        i=i,
        b_r=0.01,
        b_m=0.01,
        g=9.8,
    )


def main() -> None:
    dt = 1 / 60

    constants = get_constants()
    state = State(
        phi_d0=0,
        # XXX: Gets out of wack fairly quickly
        theta_d0=0.001,
        phi_d1=0,
        theta_d1=0,
    )
    input_val = Input(tau_0=0)

    vpython.scene.visible = False
    my_scene = vpython.canvas(width=1_000, height=1_000)  # noqa: F841
    graph = vpython.graph(  # noqa: F841
        title="Misc",
        xtitle="t",
        ytitle="Misc",
        scroll=True,
        xmin=0,
        xmax=30,
    )
    graph_phi_d0 = vpython.gcurve(color=vpython.color.red, label="phi_d0")
    graph_theta_d0 = vpython.gcurve(color=vpython.color.blue, label="theta_d0")
    graph_phi_d1 = vpython.gcurve(color=vpython.color.green, label="phi_d1")
    graph_theta_d1 = vpython.gcurve(
        color=vpython.color.orange, label="theta_d1"
    )

    body = vpython.box(
        length=constants.r * 2,
        height=l1 + l2,
        width=constants.r * 2,
        color=vpython.color.orange,
    )
    WHEEL_WIDTH = 10e-3
    wheel = vpython.cylinder(
        pos=vpython.vec(0, -body.height / 2, body.width / 2),
        axis=vpython.vec(0, 0, WHEEL_WIDTH),
        radius=constants.r,
        color=vpython.color.red,
    )
    vehicle = vpython.compound(
        [body, wheel],
        make_trail=False,
        origin=vpython.vec(0, -body.height / 2, 0),
    )

    t = 0
    while True:
        vpython.rate(1 / dt)
        # import time
        # time.sleep(1)

        # Control
        keys_down = vpython.keysdown()
        tau_0 = 0

        IMPULSE = 1e-12
        if "up" in keys_down:
            tau_0 = IMPULSE
        elif "down" in keys_down:
            tau_0 = -IMPULSE

        input_val.tau_0 = tau_0

        # Compute and integrate
        d_state = compute_derivative_state(
            constants=constants, input_val=input_val, state=state
        )
        state.phi_d1 += d_state.phi_d1 * dt
        state.phi_d0 += state.phi_d1 * dt
        state.theta_d1 += d_state.theta_d1 * dt
        state.theta_d0 += state.theta_d1 * dt

        # Apply to animation
        x = state.phi_d0 * constants.r
        vehicle.pos = vpython.vec(0, -body.height / 2, x)
        vehicle.rotate(angle=d_state.theta_d0 * dt)

        # Graph
        graph_phi_d0.plot(t, state.phi_d0)
        graph_theta_d0.plot(t, state.theta_d0)
        graph_phi_d1.plot(t, state.phi_d1)
        graph_theta_d1.plot(t, state.theta_d1)

        # Step
        t += dt

    # XXX: Next steps:
    # - [x] define reasonable constants
    # - [x] setup a visualization
    #   - [x] plot the miscellaneous things
    #   - [x] mechanism to add torque and see how it adjusts
    #   - [!] Surprise: seems numerically unstable / grows unbounded


if __name__ == "__main__":
    main()
