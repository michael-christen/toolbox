import collections
import datetime
import sys

import tabulate

from third_party.bazel.proto import build_event_stream_pb2
from utils import proto


def main() -> None:
    msgs = []
    label_to_runtime: dict[str, list[datetime.timedelta]] = (
        collections.defaultdict(list)
    )
    while msg := proto.read_delimited(
        sys.stdin.buffer, build_event_stream_pb2.BuildEvent
    ):
        msgs.append(msg)
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
    table = sorted(label_to_avg_runtime.items(), key=lambda kv: -kv[1])
    print(tabulate.tabulate(table, headers=["Label", "dt"]))


if __name__ == "__main__":
    main()
