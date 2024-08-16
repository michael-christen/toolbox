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

load("@bazel_skylib//rules:native_binary.bzl", "native_binary")

def host_console(name, binary, extra_args = []):
    """Create a host binary console run target.

    Args:
      name: target name
      binary: target binary the console is for
      extra_args: additional arguments added to the console invocation
    """
    native_binary(
        name = name,
        src = "//examples/pigweed/tools:console",
        args = [
            # This arg lets us skip manual port selection.
            "--socket",
            "default",
            "--config-file",
            "$(rootpath //examples/pigweed:pw_console_config)",
        ] + extra_args,
        data = [
            binary,
            "//examples/pigweed:pw_console_config",
        ],
    )

def device_console(name, binary, extra_args = []):
    """Create a device binary console run target.

    Makes running a console for a binary easy, and ensures the associated binary is
    up to date (but does not flash the device).

    Args:
      name: target name
      binary: target binary the console is for
      extra_args: additional arguments added to the console invocation
    """
    native_binary(
        name = name,
        src = "//examples/pigweed/tools:console",
        args = [
            "-b",
            "115200",
            "--token-databases",
            "$(rootpath " + binary + ")",
            "--config-file",
            "$(rootpath //examples/pigweed:pw_console_config)",
        ] + extra_args,
        data = [
            binary,
            "//examples/pigweed:pw_console_config",
        ],
    )
