# SBR Components

Reference photos and pin descriptions for the components used in the
Self-Balancing Robot.

## Raspberry Pi Pico 2 W

The main processor. An RP2350-based board with onboard CYW43439 for WiFi and
Bluetooth. Runs the balance control loop, PIO-based quadrature decoding, and
Pigweed RPC over UART.

```{image} ../tlbox/apps/sbr/docs/pi_pico_2_w.png
:alt: Raspberry Pi Pico 2 W pinout
:align: center
```

---

## MinIMU-9 (LSM6DSO + LIS3MDL)

6-DOF IMU (accelerometer + gyroscope) plus magnetometer in a single breakout.
Communicates over I2C (address configurable via SA0). Powered from the 3.3V
rail. Used to measure tilt angle for the balance controller.

```{image} ../tlbox/apps/sbr/docs/minimu-v9.png
:alt: MinIMU-9 breakout pinout
:align: center
```

---

## Pololu M2T550 Motoron Dual Motor Driver

Dual DC H-bridge motor driver controlled over I2C. Accepts 4.5–40V motor supply
(VM), making it compatible with a 2S LiPo directly. Drives both drive motors.
I2C address is configurable; default is 0x10.

```{image} ../tlbox/apps/sbr/docs/m2t550.png
:alt: Pololu M2T550 Motoron pinout
:align: center
```

---

## Motor Connector (Pololu 5187)

50:1 HPCB 6V DC motor with 12 CPR encoder. The connector carries two motor wires
(M1, M2), encoder power (VCC), two encoder channels (OUT A, OUT B), and ground.
At 4x quadrature decoding this gives 2400 counts/revolution.

```{image} ../tlbox/apps/sbr/docs/motor_connector.png
:alt: Motor and encoder connector wiring
:align: center
```

---

## Pololu D24V5F5 5V Buck Regulator

Fixed 5V, 500mA step-down regulator. Accepts 4–36V input — covers the full 2S
LiPo range (6.6–8.4V). Feeds the Pico W VSYS pin to produce the 3.3V logic rail
via the Pico's internal regulator.

```{image} ../tlbox/apps/sbr/docs/d24v5f5.png
:alt: Pololu D24V5F5 5V buck regulator
:align: center
```
