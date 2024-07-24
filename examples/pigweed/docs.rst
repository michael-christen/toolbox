.. _examples-01-blinky:

========================
01 - Blinky with logging
========================

Blinky introduces the basics of building, flashing and checking log
output. The instructions here will be the same for each exercise and
binary to be flashed.

Rather than sitting in a blocking loop to blink an LED, this implementation uses
timers to allow the device to do other work in between blinks.

---------------
Build and flash
---------------

#. Build the firmware with ``pw build`` or ``pw watch``.

#. Flash ``blinky.elf``.

   **STM32F429I_DISC1 (Linux/MacOS)**

   .. code-block:: sh

      pw flash --device STM32-Discovery out/gn/stm32f429i_disc1_stm32cube.size_optimized/obj/examples/01_blinky/bin/blinky.elf

   .. note::

      We don't yet have OpenOCD for Windows. See
      `b/300986008 <https://issues.pigweed.dev/300986008>`_ for updates.

   **Raspberry Pi Pico (RP2404) (Windows/Linux/MacOS)**

   1. Reboot the Pico into BOOTSEL mode by holding the bootsel button when
      plugging into USB.
   2. Copy ``./out/gn/rp2040.size_optimized/obj/examples/01_blinky/blinky.uf2``
      to your Pi Pico.

   .. note::
      It is also possible to flash a Pico board with `picotool
      <https://github.com/raspberrypi/picotool>`_. We will be adding support for
      that in this repo soon. See `b/300321451
      <https://issues.pigweed.dev/300321451>`_ for updates.

---------
View logs
---------
Logs are `tokenized <https://pigweed.dev/pw_tokenizer/>`_ and transmitted using
`pw_rpc <https://pigweed.dev/pw_rpc/>`_. If you try to view the UART output
using a serial terminal like ``minicom`` or ``screen``, the device's output
will not be human-readable because the device is sending machine-readable binary
data.

`pw_console <https://pigweed.dev/pw_console/>`_ can take this binary data and
turn it into human-readable logs and bidirectional RPC commands.

You can view the logs from your attached device with the following command:

**Device**

.. code-block:: sh

   pw console -d /dev/ttyACM0 -b 115200 --token-databases out/gn/stm32f429i_disc1_stm32cube.size_optimized/obj/examples/01_blinky/bin/blinky.elf

.. tip::

   On macOS, your device will look like ``/dev/cu.usbmodem2141403``, but
   will most likely end with a different number.

To launch the console with Bazel run:

.. code-block:: sh

   bazel run //examples/pigweed/01_blinky:console_stm32

----------------
Simulated device
----------------
The simulated device configures the porting layers (threading, communication,
timers, etc.) used by this project to rely on native implementations. This
allows you to run applications designed to run on embedded devices natively on
your computer.

In this example, the LED porting layer is set up to just emit a log message
rather than blink a physical LED.

When you launch a simulated device binary, it normally sits and waits for you
to attach `pw_console <https://pigweed.dev/pw_console/>`_ over a socket. From
the console, you'll then be able to see logs and issue commands.
``pw device-sim`` simplifies this by launching the simulated device as a
background process and then immediately launching a console session that
attaches to the simulated device.

#. Build the firmware with ``pw build`` or ``pw watch``.

#. Launch ``blinky`` using the ``pw device-sim`` helper.

   .. code-block:: sh

      pw device-sim --sim-binary ./out/gn/host_device_simulator.speed_optimized/obj/examples/01_blinky/bin/blinky

   If using Bazel launch the simulator with ``bazel run``:

   .. code-block:: sh

      bazel run //examples/pigweed/01_blinky:simulator_console

#. When you're finished, you can type ``quit`` in the ``Python Repl`` pane to
   exit.

-------------------
Building with Bazel
-------------------
To build and flash the firmware to the device run,

.. code-block:: sh

   bazel run //examples/pigweed/01_blinky:flash_stm32

Bazel knows that the flasher depends on the firmware, and will build the
firmware image before flashing it. It will also track any changes to the
firmware source and rebuild it before flashing if necessary.

If you do want to produce the `.elf` file but not flash it, run,

.. code-block:: sh

   bazel build //examples/pigweed/stm32_blinky.elf
