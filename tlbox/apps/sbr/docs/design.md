# SBR Hardware Design

Self-balancing two-wheeled robot. This document covers hardware architecture,
part selection rationale, and open decisions.

## Phased Approach

- **Phase 1 (current)**: Breadboard wiring. Schematic acts as the reference for
  connections, but no PCB yet.
- **Phase 2**: Custom PCB. Schematic gains full processor support circuitry,
  proper footprints, and layout.

---

## Components

| Subsystem        | Part                                    | Notes |
|------------------|-----------------------------------------|-------|
| Processor        | Raspberry Pi Pico W                     | Breadboard: pin headers. PCB: castellated pads soldered down. |
| IMU              | MinIMU-9 (LSM6DSO + LIS3MDL) breakout  | For PCB v2: bare LSM6DSO + LIS3MDL. |
| Motor driver     | Pololu M2T550 Motoron                   | I2C, dual DC H-bridge. |
| Motors           | Pololu 5187 (50:1 HPCB 6V, 12 CPR)    | 6V rated. See firmware duty-cycle limit below. |
| Battery          | 2S LiPo, ~1000mAh                      | 7.4V nominal, 8.4V full. Connector per pack (XT30 typical). |
| Logic supply     | 5V buck (e.g. Pololu D24V5F5)          | 4–36V input range covers full 2S charge. Feeds Pico W VSYS. |

- **Mechanical**: [OnShape model](https://cad.onshape.com/documents?nodeId=2f14397cff1201652b29e7ee&resourceType=folder)

### Motor encoder note

12 CPR on the motor shaft × 50:1 gear ratio × 4x quadrature decoding =
**2400 counts/wheel revolution**. Excellent resolution for velocity estimation.
Pico PIO handles quadrature decoding without CPU overhead.

---

## Power Architecture

```
2S LiPo (7.4V nom)
    |
    +---> M2T550 Motoron (motor power, 4.5–40V input)
    |
    +---> 5V buck converter
              |
              +---> Pico W VSYS (1.8–5.5V input, internal RT6150 regulator)
                        |
                        +---> 3.3V rail (Pico W 3V3 output)
                                  |
                                  +---> IMU (MinIMU-9)
                                  +---> Encoders
                                  +---> UART radio
```

**Notes:**
- The Pico W's internal RT6150 buck-boost produces the 3.3V logic rail.
  Feed VSYS only, not the 3V3 pin directly.
- Add a 1000µF electrolytic capacitor close to the M2T550 for motor switching
  noise. The M2T550 also requires its own bulk cap per its datasheet.
- An LDO from the battery to 3.3V is not viable: at 8.4V → 3.3V × 200mA =
  1.0W dissipated as heat, and worse at higher voltages.

### Firmware duty-cycle limit

Motor rated voltage: 6V. Max battery voltage: 8.4V (full charge).
Maximum safe duty cycle at full charge: `6.0 / 8.4 ≈ 71%`. As the battery
discharges the limit relaxes — at nominal (7.4V) it's ~81%, and near cutoff
(~6.6V) it approaches 100%. Control authority is adequate across the usable
battery range. The cap should still be implemented as a named constant in the
motor driver layer to protect against running off a freshly charged pack.

---

## Communications

### Bench debugging (USB)

The Pico W presents as a USB CDC serial port natively via `pico_stdio_usb` — no
additional hardware required. BOOTSEL reprogramming also uses USB. The USB
connector on the Pico W module is the bench interface; no schematic work needed
beyond ensuring physical access.

### Wireless telemetry (UART radio)

**Part**: HexTronik 433MHz radio set (SiK firmware, transparent UART mode).
- Air module mounts on the robot; ground module plugs into the PC via USB-UART.
- Operates at 3.3V logic — directly compatible with Pico W GPIO, no level
  shifting needed.
- Configured via AT commands; in transparent mode it is invisible to firmware.
- Connected to **UART0** on the Pico W.

**Topology**: USB CDC and UART0 radio are independent, always-active transports.
No muxing or switching logic needed. In Pigweed, configure the RPC/HDLC
transport to use UART0; stdio can also mirror to USB CDC.

Fallback: HC-12 module is a drop-in alternative on the robot side, we'd need to
configure it on the host side.

### RC controller (Phase 1–4)

**Part**: HK-T4A V2 2.4GHz receiver.
- Outputs standard PWM (1–2ms pulses) or PPM sum per channel.
- Pico PIO reads PWM/PPM with microsecond accuracy, zero CPU overhead.
- 4 channels: throttle/forward, steering, kill switch, mode select.
- No firmware stack, no pairing complexity. Ideal for bringup.

### Gamepad controller (Phase 5)

**Part**: DualShock 4 (CUH-ZCT2U) via Bluepad32.
- Uses BT Classic HID over the CYW43439 on the Pico W.
- CYW43439 handles BT in its own processor; RP2040 receives SPI callbacks only.
  Control loop impact is minimal but untested — defer until robot is balancing.
- Proof-of-concept exists in `~/tmp/bluepad32`.
- Note: simultaneous BT + WiFi on the CYW43439 has known instability. If WiFi
  telemetry is also active, test this combination explicitly.

---

## Electrical Interface Summary

### I2C bus (I2C0)

All I2C peripherals share a single bus. Pull-ups: 4.7kΩ to 3.3V.

| Device         | Address      |
|----------------|--------------|
| M2T550 Motoron | 0x10 (default, configurable) |
| LSM6DSO        | 0x6A or 0x6B (SA0 pin) |
| LIS3MDL        | 0x1C or 0x1E (SA1 pin) |

### PIO / GPIO

| Signal              | Interface | Pins       |
|---------------------|-----------|------------|
| Motor A encoder A/B | PIO       | 2 pins     |
| Motor B encoder A/B | PIO       | 2 pins     |
| RC receiver PPM/PWM | PIO       | 1–4 pins   |

### UART

| Signal      | Peripheral      | UART     |
|-------------|-----------------|----------|
| TX/RX radio | HexTronik radio | UART0    |

---

## Schematic Corrections Needed

The current `pcb_v1` schematic has several incorrect parts that must be replaced
before PCB layout:

| Sheet           | Current part          | Correct part                        |
|-----------------|-----------------------|-------------------------------------|
| `imu`           | MPU-9250 (QFN-24)     | LSM6DSO + LIS3MDL (or MinIMU-9 breakout connector) |
| `stepper_motor` | DRV8825 stepper driver | M2T550 Motoron breakout             |
| `uart_radio`    | Bare 2-pin connector  | HexTronik/SiK module connector (with power + UART pins) |
| Top-level       | *(missing)*           | Battery connector, 5V buck, power rails |
| `processor`     | *(incomplete)*        | Full Pico W castellated pad footprint for PCB phase |

---

## Open Items

- [ ] Confirm I2C address configuration on M2T550 (check solder jumpers on board vs default address)
- [ ] Measure HexTronik radio logic voltage to confirm 3.3V (not 5V)
- [ ] PCB phase: add reverse-polarity protection (P-channel MOSFET on battery input) and power LED
