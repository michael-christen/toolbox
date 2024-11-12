# Logs

Just miscellaneous, project specific thoughts / notes. Mostly for my own
internal use.

### 2024-10-25, Friday:

- Making a new pigweed app
  - Do I need a new system for each new app?
    - I'm not quite sure, maybe it is thinking of each as a separate target
      layout?
    - I think we could probably leave it as Init/Start and leave it at that
    - May be able to completely avoid to start (though probably want for host)
- 22:34 - spending a lot of time trying to find the pigweed module to describe a
  register map
  - 22:53 - found it in 3rd party libraries:
    https://github.com/google/emboss/blob/master/doc/guide.md

### 2024-10-26, Saturday:

- having trouble getting data out of pdf, tried using chat gpt, but it only
  really got a few rows
  - pdftotext worked fairly well, but still a fair amount of manual intervention
- this is taking a while, worth reconsidering my approach; let's look at
  existing libraries at least for inspiration, if not for data ingestion
- separately, I notice when I dive into this stuff, I leave a wake of way too
  many tabs, which eventually slows me down

- I'm considering how to perform encoder readings. Here are some references on
  PIO
  - https://blues.com/blog/raspberry-pi-pico-pio/
  - https://rp2040pio-docs.readthedocs.io/en/latest/
  - https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf
  - https://github.com/p-o-l-e/quadrature-decoder
  - https://github.com/jamon/pi-pico-pio-quadrature-encoder
  - https://blog.domski.pl/quadrature-encoders-with-raspberry-pi-pico-pio/
  - other articles about reading encoders:
    - https://makeatronics.blogspot.com/2013/02/efficiently-reading-quadrature-with.html
- I don't think I'll be able to easily do non-blocking i2c out of the box, I may
  need to adjust things a bit
- other self-balancing robots:

  - https://blog.pictor.us/self-balancing-robot/
  - https://blog.pictor.us/lqr-control-of-a-self-balancing-robot/

- Alternatives to emboss's approach for bit-packing
  - union bitfields
  - enums / constants
  - don't even separate bit-fields
  - C++ templated bitfields:
    https://codereview.stackexchange.com/questions/54342/template-for-endianness-free-code-data-always-packed-as-big-endian
  - structuring this information in a machine-readable way that can easily
    generate code doesn't seem to be solved / there are probably some other good
    repos out there
    - https://docs.python.org/3/library/struct.html is python's approach to it

Alright, before spending a bunch of time merely transcribing these fields into
code, let's get working knowledge for how these work, taking a look at:

- application note
- datasheet
- exisiting code (should help me narrow down on what I need to care about)

Alright, let's start with this AHRS (Attitude and Heading Reference System)
application:

https://github.com/pololu/minimu-9-ahrs-arduino.

- could be handy for a sanity check on hardware setup

- setup
  - init
    - accel
    - compass
    - gyro
  - calibrate (32 readings) to determine offsets to apply
    - note: lots of delays there
    - read_gyro
    - read_accel
- loop (50 Hz)

  - read others + compass and get compass_heading
  - mathematics to update matrix, normalize, drift correction and compute euler
    angles
  - could probably run faster?

- accel / gyro init
  - gyro_acc.init(), .enableDefault()
  - `gyro_acc.writeReg(LSM6::CTRL1_XL, 0x3C); // 52 Hz, 8 g full scale`
- accel init

  - check address and read `WHO_AM_I (0x0F)` register
  - there are a few different behaviors based on whether we're a specific device
    type, the library auto-detects by checking `WHO_AM_I`

- accel/gyro `enable_default`
  - pick resolution and rate
  - auto-increment register address for multiple byte access
    - they use this for readAcc, etc.

```
/*
Enables the LSM6's accelerometer and gyro. Also:
- Sets sensor full scales (gain) to default power-on values, which are
  +/- 2 g for accelerometer and 245 dps for gyro
- Selects 1.66 kHz (high performance) ODR (output data rate) for accelerometer
  and 1.66 kHz (high performance) ODR for gyro. (These are the ODR settings for
  which the electrical characteristics are specified in the LSM6DS33 datasheet.)
- Enables automatic increment of register address during multiple byte access
Note that this function will also reset other settings controlled by
the registers it writes to.
*/

    // Accelerometer

    // 0x80 = 0b10000000
    // ODR = 1000 (1.66 kHz (high performance)); FS_XL = 00 (+/-2 g full scale)
    writeReg(CTRL1_XL, 0x80);

    // Gyro

    // 0x80 = 0b010000000
    // ODR = 1000 (1.66 kHz (high performance)); FS_G = 00 (245 dps for DS33, 250 dps for DSO)
    writeReg(CTRL2_G, 0x80);

    // Common

    // 0x04 = 0b00000100
    // IF_INC = 1 (automatically increment register address)
    writeReg(CTRL3_C, 0x04);
```

- readACC
  - write `OUTX_L_XL` to specify register, then read 6 bytes (2 for each of
    x,y,z); combine bytes
  - they aren't waiting for data to be ready?
- readGyro

  - same process for gyro

- thoughts?

  - I may be able to structure my data type to read and format it for myself,
    without needing to shift afterwards

- compass
  - same detection of address and type

```
/*
Enables the LIS3MDL's magnetometer. Also:
- Selects ultra-high-performance mode for all axes
- Sets ODR (output data rate) to default power-on value of 10 Hz
- Sets magnetometer full scale (gain) to default power-on value of +/- 4 gauss
- Enables continuous conversion mode
Note that this function will also reset other settings controlled by
the registers it writes to.
*/
    // 0x70 = 0b01110000
    // OM = 11 (ultra-high-performance mode for X and Y); DO = 100 (10 Hz ODR)
    writeReg(CTRL_REG1, 0x70);

    // 0x00 = 0b00000000
    // FS = 00 (+/- 4 gauss full scale)
    writeReg(CTRL_REG2, 0x00);

    // 0x00 = 0b00000000
    // MD = 00 (continuous-conversion mode)
    writeReg(CTRL_REG3, 0x00);

    // 0x0C = 0b00001100
    // OMZ = 11 (ultra-high-performance mode for Z)
    writeReg(CTRL_REG4, 0x0C);

    // 0x40 = 0b01000000
    // BDU = 1 (block data update)
    writeReg(CTRL_REG5, 0x40);
```

- writes MSB to get subaddress updating? Is that auto-incrementing?

```
  // assert MSB to enable subaddress updating
  Wire.write(OUT_X_L | 0x80);
  Wire.endTransmission();

  Wire.requestFrom(address, (uint8_t)6);
```

- there is temperature data
- the compass is fairly straightforward
- In order to read multiple bytes, it is necessary to assert the most
  significant bit of the subaddress field. In other words, SUB(7) must be equal
  to 1, while SUB(6-0) represents the address of first register to be read.

  - See 5.1.1 I2C operation of LIS3MDL data sheet

- there are self-test features on these chips

So, let's write-up a proto interface for these.

- [ ] Where to put common references:
      https://jpa.kapsi.fi/nanopb/docs/concepts.html
  - the hardest part of documentation is making it useful in the future
- [ ] we should have 2 different endianness processors to ensure we're properly
      handling endianness and not relying on processor specifics
- [ ] Is there a good/uniform way to encode state machines?
- [ ] I wonder what happens if BDU and FAST_READ are set at the same time, would
      it not update?

- what is emboss gonna be like / how parseable is it, eg) if I wanted to make my
  own frontend, could that work? Is it inefficient?

  - enums are uint64 when uint8 would suffice

- [ ] emboss doesn't enforce fields don't overlap ...
- [ ] seeing very long link times when making / editing tests
  - if I disable remote caching, the speed is fine ...

### 2024-10-27, Sunday:

- https://protobuf.dev/reference/cpp/api-docs/google.protobuf.repeated_field/#RepeatedField
- https://github.com/catchorg/Catch2/blob/devel/docs/assertions.md

### 2024-10-30, Wednesday:

- pigweed pw::Status https://pigweed.dev/pw_status/reference.html#c.OK
  - OK, CANCELLED, UNKNOWN, INVALID_ARGUMENT, DEADLINE_EXCEEDED, NOT_FOUND,
    ALREADY_EXISTS, PERMISSION_DENIED, RESOURCE_EXHAUSTED, FAILED_PRECONDITION,
    ABORTED, OUT_OF_RANGE, UNIMPLEMENTED, INTERNAL, UNAVAILABLE, DATA_LOSS,
    UNAUTHENTICATED,
- would be good to read more about `pw_rpc`
- got the server running (had odd issues when both the C++ and nanopb libraries
  were included)
- InterpretReading is crashing on uninitialized values

- [ ] It'd be a good idea to make a host/simulation initiator for i2c, then I
      could run simulator_binary and actually have it fill with useful
      information.

  - should do a little write-up on pigweed's approach in sense (fake definitions
    for most things at the application level)

- next step, let's run it on some hardware!
  - revisit full sim afterwards
  - need to setup device

### 2024-10-31, Thursday:

describe pigweed's sense firmware layout

- apps
  - build for end application + main.cc
    - register services and start system
    - int main or InitializeApp (unclear which to choose)
      - just call from main
  - (can have multiple apps built for a single system), different than work's
    position
  -
- device
  - most of the hardware specific things, eg) the sensors + pico
- modules
  - lots of different ones, neat constructs for async, timing, etc.
  - individual modules can have services, etc.
  - board refers to the pico board, not the pcb it's on
  - lots of fakes
  - morse code :) constexpr pw::containers::FlatMap seems neat
  - a neat little pubsub + button management
  - sampling thread for sensor
  - example of .options file
  - worker + timer
  - [ ] (really, just most of the goodies, got to figure out how they're wired
        up)
- system
  - high-level definition of system (what components), + pubsub + worker
- targets -> malloc alias, host + rp2 descriptions
  - define target-dependent system (reference the "fake" modules)
  - host: pick fake modules, setup ctrl-c handler, print instructions, call
    SystemStart, setup memory allocation and stream channel
  - rp2: FreeRTOS config, override platform flags
    - define rp2040_binary and rp2350_binary
    - define platform, tests, + system
      - [ ] separating the common platform from the system definition could be
            handy
        - where is unit_test_rpc_main used?
- tools -> console setup, Device examples + connection, factory
- `web_app` -> ignore

### 2024-11-03, Sunday:

- I got cross-compilation working and gyro at first wasn't acknowledging, but
  now it's working after debugging with waveforms
- y seems to have different offsets than x and z, x and z are largely negative.
  - would be good to corroborate with arduino application

### 2024-11-06, Wednesday:

- ran arduino tools, saw similar behavior; seems like we need a calibration
  process and offset

### 2024-11-07, Thursday:

breakup the diff: https://github.com/michael-christen/toolbox/pull/136/files

- add `--config local` approach for bypassing bes/remote cache when network is
  slow
- add `hw_services/sbr/sbr.proto`
- add `emboss`
  - why do we need `enable_enum_traits = False`?
- add apps/sbr
- update platform to allow us to make new ones per system
- good documentation on lis3mdl
- host i2c initiator
- platform definitions
- clang-format

TODO:

- [x] maybe move more pigweed things to third party?
- [x] make hw_service plural
- [>] make common host_system library?
- [x] clang-format
- [x] remove production_app_threads for now

Followup:

- [>] how to specify fixed size on nanopb repeated with options?
  - can't get it to work, got proto_library to work, didn't know how to include
    options
  - could try with
    load("@com_github_nanopb_nanopb//extra/bazel:nanopb_cc_proto_library.bzl",
    "cc_nanopb_proto_library")
- [>] gazelle cc_library for sbr
- [>] nanopb, change generated code suffix
- stream meaasurements
- state machine
- configuration
- test where we spin up the firmware
- compare select vs. label_flag