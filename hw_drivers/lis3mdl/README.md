# LIS3MDL Magnetometer

Reference:

- https://www.pololu.com/file/0J1089/LIS3MDL.pdf
- https://www.pololu.com/file/0J1090/LIS3MDL-AN4602.pdf

Data style is a lot of 16-bit 2's complement.

Register study:

- (0x05 - 0x0A): Offset Management
  - OUT = OUT_measured - OFFSET
- (0x0F ): WHO_AM_I = (0x3D)
- (0x20 - 0x24): CTRL_REG[1-5]
  - Output Data Rate (Hz): (0.625, 1.25, 2.5, 5, 10, 20, 40, 80, 1000, 560,
    300, 155)
  - Operating Modes: (LOW_POWER, MEDIUM_PERFORMANCE, HIGH_PERFORMANCE,
    ULTRA_HIGH_PERFORMANCE)
    - x/y are independent from z
  - Full Scale: (4, 8, 12, 16)
  - Measurement Mode
- (0x27 ): STATUS_REG
- (0x28 - 0x2D): OUT_X/Y/Z for magnetometer
- (0x2E - 0x2F): TEMP_OUT
- (0x30 - 0x33): Interrupt Management

Table 5: Noise in operating modes (average per axis)

Table 8: Turn-on time

| Operating mode         | RMS noise [mgauss] | Startup time [us] |
| ---------------------- | ------------------ | ----------------- |
| Ultra-high-performance | 3.5                | 6,650             |
| High-performance       | 4.0                | 3,480             |
| Medium-performance     | 4.6                | 1,910             |
| Low-power              | 5.3                | 1,200             |

- Not shown here
  - TON (table 9)
  - 2D table of ODR vs. Mode to current consumption

State machine

```
STARTUP -> IDLE;
SINGLE_MEASUREMENT -> IDLE (edge = single-measurement mode);
(ANY) -> IDLE (edge = MD1 bit high);

IDLE - 1 uA
SINGLE_MEASUREMENT
CONTINUOUS_MEASUREMENT
```

Startup sequence:

- Power supply set
- Power on, reset rising
- Boot procedure from flash
- Single Measure
- Idle State
- ? Unclear if DRDY is set?

Commands to send for startup:

1. CTRL_REG2(0x40) // full scale +/- 12 Hz
2. CTRL_REG1(0xFC) // UHP on X/Y, ODR @ 80 Hz + temperature
3. CTRL_REG4(0x0C) // UHP on Z
4. CTRL_REG3(0x00) // CONTINUOUS_MEASUREMENT mode

Reading

- DRDY goes high when new data, and low when read
  - via pin or STATUS_REG
  - STATUS_REG also conveys whether we missed any samples

Options:

- Should set BDU (block data update) to avoid `_L and _H` section changing while
  reading
- FAST_READ discards the L values
- BLE can change endianness of `_L and _H`

Interrupts: We won't use now, but could be a neat low-power mechanism to detect
a re-orientation

Self-Test

- This test is enabled by setting bit 0 to ‘1’ in the CTRL_REG1 (20h) register.
- Keep device still during self-test

```
1. Write 1Ch to CTRL_REG1(20h)
1. Write 40h to CTRL_REG2(21h)
1. Wait 20ms
1. Write 00h to CTRL_REG3(22h)

Initialize Sensor, turn on sensor.
FS=12Gauss, Continuous-Measurement mode, ODR = 80Hz


Power up, wait 20ms for stable output

Check ZYXDA in STATUS_REG (27h) – Data Ready Bit
Read OUT_X_L(28h), OUT_X_H(29h), OUT_Y_L(2Ah), OUT_Y_H(2Bh), OUT_Z_L(2Ch), OUT_Z_H(2Dh) → Discard data
- Reading OUTX/OUTY/OUTZ clears ZYXDA. Wait for the first sample.

// Read the output registers after checking ZYXDA bit 5 times
Read OUT_X_L(28h), OUT_X_H(29h): Store data in OUTX_NOST
Read OUT_Y_L(2Ah), OUT_Y_H(2Bh): Store data in OUTY_NOST
Read OUT_Z_L(2Ch), OUT_Z_H(2Dh): Store data in OUTZ_NOST
// Average the stored data on each axis.

Write 10h to CTRL_REG1(20h)
// Enable Self Test
Wait for 60 ms

Check ZYXDA in STATUS_REG (27h) – Data Ready Bit
// Reading OUTX/OUTY/OUTZ clears ZYXDA. Wait for the first sample.
Read OUT_X_L(28h), OUT_X_H(29h), OUT_Y_L(2Ah), OUT_Y_H(2Bh), OUT_Z_L(2Ch), OUT_Z_H(2Dh) → Discard data


// Read the output registers after checking ZYXDA bit * 5 times
Read OUT_X_L(28h), OUT_X_H(29h): Store data in OUTX_ST
Read OUT_Y_L(2Ah), OUT_Y_H(2Bh): Store data in OUTY_ST
Read OUT_Z_L(2Ch), OUT_Z_H(2Dh): Store data in OUTZ_ST
// Average the stored data on each axis.

pass = compare min(st_?) <= out?_ST - out?_NOST <= max(st_?)

Write 1Ch to CTRL_REG1(20h): Disable self-test
Write 03h to CTRL_REG3(22h): Power-down mode
```

Self-test limits

| Axis | MIN [gauss] | MAX [gauss] |
| ---- | ----------- | ----------- |
| X    | 1.0         | 3.0         |
| Y    | 1.0         | 3.0         |
| Z    | 0.1         | 3.0         |

Temperature can be enabled/disabled, 0 = 25 C, 1/8 C per LSB, the magnetometer
uses temperature compensation

I2C address is `0b001_1x0`, x pased on SDO/SA1 pin

Magnitude of Earth's magnetic field at surface ranges from 0.25 to 0.65 Gauss.
I'm not sure if motors will render this less useful.

Tests

- [ ] self-test procedure
- [ ] power motors near magnetometer and view output / characterize noise
- [ ] Characterization. Sweep across resolutions, etc. and graph the output
      stable and on lazy susan?
