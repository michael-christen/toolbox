# Register Description Format Experiment

Evaluation of SVD vs SystemRDL for describing peripheral registers in the SBR
embedded project. Tracks issue #330.

## Files

| File | Purpose |
|------|---------|
| `lsm6dso_subset.rdl` | SystemRDL description (PeakRDL input) |
| `lsm6dso_subset.svd` | SVD description (same registers, XML format) |
| `lsm6dso_subset.h` | Generated C header (from SystemRDL via PeakRDL) |
| `html_docs/` | Generated HTML register docs (from SystemRDL) |

The example models a representative subset of the LSM6DSO IMU registers:
`WHO_AM_I`, `CTRL1_XL`, `CTRL2_G`, `STATUS_REG`, and the six gyro/accel
output byte registers — the exact registers used by the SBR balance controller.

## Tooling Used

```
peakrdl==1.5.0          # SystemRDL toolchain
svdtools==0.1.27        # SVD validation and memory map
systemrdl-compiler==1.32.2  # PeakRDL dependency
```

Not yet in `requirements.in` (see Bazel integration section below).

## Generating Artifacts

```bash
# C header from SystemRDL
peakrdl c-header lsm6dso_subset.rdl -o lsm6dso_subset.h --bitfields ltoh

# HTML documentation from SystemRDL
peakrdl html lsm6dso_subset.rdl -o html_docs/

# Memory map from SVD
svd mmap lsm6dso_subset.svd

# Validate SystemRDL model
peakrdl dump lsm6dso_subset.rdl
```

## Format Comparison

### File size (same registers)

| Format | Lines | Bytes |
|--------|-------|-------|
| SystemRDL | 156 | 6,374 |
| SVD (XML) | 212 | 12,317 |

SVD is ~2x the size for identical coverage, almost entirely due to XML
verbosity (repeated `<name>`, `<value>`, `<description>` tags per enum entry).

### Expressiveness

**SystemRDL advantages:**
- Define an enum type once (`odr_xl_e`) and bind it to a field via `encode`.
  In SVD you copy-paste the full `<enumeratedValues>` block for every field
  that shares the same encoding.
- Inheritance and parameters (not needed here but useful at scale).
- Built-in reset value defaults (`default hw = r; default sw = rw;`).
- Compact addressing directive removes manual gap calculations.

**SVD advantages:**
- XML is universally editable; no new language to learn.
- svd2rust generates type-safe Rust PAC crates — the standard approach in
  embedded Rust (e.g., all RP2350 ecosystem crates use the official
  Raspberry Pi SVD).
- IDE register viewers (Cortex-Debug, Ozone, J-Link) read SVD directly.

### Tooling output

| Output | SystemRDL/PeakRDL | SVD |
|--------|-------------------|-----|
| C header | ✓ (`peakrdl c-header`) | via svd2c or manual |
| HTML docs | ✓ (`peakrdl html`) | — |
| UVM model | ✓ (`peakrdl uvm`) | — |
| SystemVerilog | ✓ (`peakrdl regblock`) | — |
| IP-XACT | ✓ (`peakrdl ip-xact`) | — |
| Rust PAC | — | ✓ (`svd2rust`) |
| IDE register view | — | ✓ (Cortex-Debug etc.) |
| SVD output | — (no PeakRDL plugin) | native |

### Key gotcha: SystemRDL field ordering

SystemRDL auto-packs fields from bit 0 upward. Fields must be declared
**LSB-first** to match hardware register layout:

```systemrdl
// WRONG: declares ODR_XL at bits [3:0] instead of [7:4]
field {encode = odr_xl_e;} ODR_XL[4] = 4'h4;
field {encode = fs_xl_e;}  FS_XL[2]  = 2'h2;
field {} LPF2_XL_EN[1] = 1'b0;
field {} rsvd0[1] = 1'b0;

// CORRECT: auto-pack from bit 0 → ODR_XL lands at bits [7:4]
field {} rsvd0[1] = 1'b0;      // bit [0]
field {} LPF2_XL_EN[1] = 1'b0; // bit [1]
field {encode = fs_xl_e;}  FS_XL[2]  = 2'h2; // bits [3:2]
field {encode = odr_xl_e;} ODR_XL[4] = 4'h4; // bits [7:4]
```

Alternatively, use explicit `@bit_offset` or declare the addrmap with a
`lsb0` property and write fields MSB-first. The LSB-first convention is less
surprising once you know it.

## Recommendation

**Use SystemRDL/PeakRDL for external peripheral register descriptions in this
project.**

Rationale:
1. **Primary output is C headers.** PeakRDL's `c-header` plugin generates
   well-structured unions with bitmask/bitposition macros and a packed struct
   for field access — exactly what C++ firmware needs. SVD has no good C
   generator.
2. **More maintainable at scale.** Enum reuse and defaults reduce copy-paste
   errors across a multi-register peripheral like LSM6DSO (~128 registers
   total).
3. **HTML docs are free.** Running `peakrdl html` produces a browsable
   register reference that's useful during driver development.
4. **SVD is already covered for internal peripherals.** The RP2350 official
   SVD handles the chip's own peripherals (SPI, I2C, PIO, etc.). There's no
   need to author SVD for the MCU itself.

SVD remains the right choice if/when the project adds Rust firmware (for
svd2rust PAC generation) or wants IDE register-level debugging via Cortex-Debug.

## Bazel Integration

`peakrdl` and `svdtools` need to be added to `requirements.in` before the
genrules in `BUILD` will work:

```
# requirements.in
peakrdl
svdtools
```

Then:
```bash
bazel run //:requirements.update
bazel run //:gazelle_python_manifest.update
```

The genrule approach works for one-off generation. For production use,
consider a custom Bazel rule (similar to `//bzl:py.bzl`) that wraps
`peakrdl c-header` as a proper build action with hermetic inputs/outputs.
