# SBR Roadmap

A self-balancing two-wheeled robot built on the Raspberry Pi Pico W with
closed-loop balance control, WiFi telemetry, and Bluetooth gamepad support.

## Phase 1: Hardware Bringup, Drivers, and Simulation

Build out the v1 schematic, breadboard, and configure drivers.

Each peripheral needs a C++ driver and a software simulator so the control
stack can be tested on a host without hardware.

| Issue | Title |
|-------|-------|
| [#302](https://github.com/michael-christen/toolbox/issues/302) | SimLsm6dso I2C initiator (test double for LSM6DSO) |
| [#309](https://github.com/michael-christen/toolbox/issues/309) | M2T550 (Motoron) C++ I2C driver + SimM2t550 |
| [#310](https://github.com/michael-christen/toolbox/issues/310) | LSM6DSO gyro/accelerometer driver |
| [#311](https://github.com/michael-christen/toolbox/issues/311) | Encoder reading (quadrature decoder via Pico PIO) |

## Phase 2: Service Layer

The RPC service is the interface between firmware and host tooling. Expand it
to cover all sensors and actuators so the robot can be commanded and observed
over the wire.

| Issue | Title |
|-------|-------|
| [#312](https://github.com/michael-christen/toolbox/issues/312) | Expand SBR RPC service: IMU, motor control, encoders |

## Phase 3: Control System

The core of the project. Two nested loops: an inner balance loop (pitch → motor
speed) and an outer velocity loop (encoder velocity → balance setpoint).

| Issue | Title |
|-------|-------|
| [#313](https://github.com/michael-christen/toolbox/issues/313) | IMU sensor fusion — complementary filter for pitch angle |
| [#314](https://github.com/michael-christen/toolbox/issues/314) | PID balance controller (inner + velocity loop) |

## Phase 4: Mechanical Build

- [ ] Finish modelling, print chassis and assemble

## Phase 5: Comms & UX

With the robot balancing, close the feedback loop for tuning and add manual
control.

| Issue | Title |
|-------|-------|
| [#315](https://github.com/michael-christen/toolbox/issues/315) | WiFi telemetry streaming for real-time PID tuning |
| [#316](https://github.com/michael-christen/toolbox/issues/316) | Bluetooth gamepad interface |

## Phase 6: Integration & Bringup

Once hardware arrives, work through systematic bringup before running the
full control stack.

| Issue | Title |
|-------|-------|
| [#317](https://github.com/michael-christen/toolbox/issues/317) | Hardware bringup checklist |

## Phase 7: Hardware - PCB

Create the finalized PCB

| Issue | Title |
|-------|-------|
| [#305](https://github.com/michael-christen/toolbox/issues/305) | Hermetic KiCad installation (reproducible builds) |
| [#307](https://github.com/michael-christen/toolbox/issues/307) | PCB layout / routing |
| [#308](https://github.com/michael-christen/toolbox/issues/308) | PCB review, DRC, and fabrication order |
