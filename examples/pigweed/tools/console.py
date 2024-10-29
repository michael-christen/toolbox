# Copyright 2024 The Pigweed Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Wraps pw_system's console to inject quickstart's RPC proto."""

import argparse
import logging
import sys

import pw_cli
import pw_system.console
from pw_system.device import Device as PwSystemDevice
from pw_system.device_connection import DeviceConnection
from pw_system.device_connection import add_device_args
from pw_system.device_connection import (
    create_device_serial_or_socket_connection,
)

from examples.pigweed.modules.blinky import blinky_pb2
from hw_service.sbr import sbr_pb2

_LOG = logging.getLogger(__file__)


# Quickstart-specific device classes, new functions can be added here.
# similar to ones on the parent pw_system.device.Device class:
# https://cs.opensource.google/pigweed/pigweed/+/main:pw_system/py/pw_system/device.py?q=%22def%20run_tests(%22
class Device(PwSystemDevice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def toggle_led(self):
        """Toggles the onboard (non-RGB) LED."""
        self.rpcs.blinky.Blinky.ToggleLed()

    def set_led(self, on: bool):
        """Sets the onboard (non-RGB) LED."""
        self.rpcs.blinky.Blinky.SetLed(on=on)

    def blink(self, interval_ms=1000, blink_count=None):
        """Sets the onboard (non-RGB) LED to blink on and off."""
        self.rpcs.blinky.Blinky.Blink(
            interval_ms=interval_ms, blink_count=blink_count
        )

COMPILED_PROTOS = [
    blinky_pb2,
    sbr_pb2,
]

def get_device_connection(
    setup_logging: bool = True,
    log_level: int = logging.DEBUG,
) -> DeviceConnection:
    if setup_logging:
        pw_cli.log.install(level=log_level)

    parser = argparse.ArgumentParser(
        prog="quickstart",
        description=__doc__,
    )
    parser = add_device_args(parser)
    args, _remaning_args = parser.parse_known_args()

    device_context = create_device_serial_or_socket_connection(
        device=args.device,
        baudrate=args.baudrate,
        token_databases=args.token_databases,
        compiled_protos=COMPILED_PROTOS,
        socket_addr=args.socket_addr,
        ticks_per_second=args.ticks_per_second,
        serial_debug=args.serial_debug,
        rpc_logging=args.rpc_logging,
        hdlc_encoding=args.hdlc_encoding,
        channel_id=args.channel_id,
        # Device tracing is not hooked up yet for Pigweed Sense.
        device_tracing=False,
        device_class=Device,
    )

    return device_context


def main() -> int:
    return pw_system.console.main(
        compiled_protos=COMPILED_PROTOS,
        device_connection=get_device_connection(),
    )


if __name__ == "__main__":
    sys.exit(main())
