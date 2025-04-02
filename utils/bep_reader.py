"""An example application that reads BEP binary files.

This logs a nice table of targets' average test run time sorted by slowest
first.

Example:
> bazel test //... --build_event_binary_file=test_all.pb
> bazel run //utils:bep_reader < test_all.pb
>

 Label                                          dt
 ---------------------------------------------  --------------
 //:requirements_test                           0:01:20.341000
 //examples/pigweed/modules/blinky:blinky_test  0:00:03.611000
 //utils:graph_algorithms_test                  0:00:00.650000
"""

import collections
import datetime
import io
import sys
from typing import BinaryIO

import tabulate
import zstandard

from third_party.bazel.proto import build_event_stream_pb2
from third_party.bazel.proto import spawn_pb2
from third_party.delimited_protobuf import delimited_protobuf


def get_label_to_runtime(buf: BinaryIO) -> dict[str, datetime.timedelta]:
    label_to_runtime: dict[str, list[datetime.timedelta]] = (
        collections.defaultdict(list)
    )
    while msg := delimited_protobuf.read_delimited(
        buf, build_event_stream_pb2.BuildEvent
    ):
        msg_id = msg.id.WhichOneof("id")
        if msg_id == "test_result":
            # Only register succesful tests
            if msg.test_result.status != build_event_stream_pb2.PASSED:
                continue
            label = msg.id.test_result.label
            dt = msg.test_result.test_attempt_duration.ToTimedelta()
            # Accumulate multiple
            label_to_runtime[label].append(dt)
            # Could capure cache stae with cached_locally
    label_to_avg_runtime = {}
    for label, runtimes in label_to_runtime.items():
        total_runtime = datetime.timedelta(0)
        for runtime in runtimes:
            total_runtime += runtime
        label_to_avg_runtime[label] = total_runtime / len(runtimes)
    return label_to_avg_runtime


def get_label_to_buildtime_from_compact_exec_log(
    buf: BinaryIO,
) -> dict[str, datetime.timedelta]:
    dctx = zstandard.ZstdDecompressor()
    decompressed_data = io.BytesIO()
    dctx.copy_stream(buf, decompressed_data)
    decompressed_data.seek(0)
    label_to_buildtime = {}
    while msg := delimited_protobuf.read_delimited(
        decompressed_data, spawn_pb2.ExecLogEntry
    ):
        if msg.HasField("spawn"):
            label = msg.spawn.target_label
            if label in label_to_buildtime:
                raise AssertionError(
                    f"Expected label {label} to be unique in exec log"
                )
            label_to_buildtime[msg.spawn.target_label] = (
                # Could consider execution_wall_time instead of total?
                msg.spawn.metrics.total_time.ToTimedelta()
            )
    return label_to_buildtime


def main() -> None:
    buf = sys.stdin.buffer
    label_to_avg_runtime = get_label_to_runtime(buf)
    table = sorted(label_to_avg_runtime.items(), key=lambda kv: -kv[1])
    print(tabulate.tabulate(table, headers=["Label", "dt"]))


if __name__ == "__main__":
    main()
