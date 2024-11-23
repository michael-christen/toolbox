import sys

import tabulate

from utils import proto
from third_party.bazel.proto import build_event_stream_pb2

def main() -> None:
    msgs = []
    label_to_runtime = {}
    while msg := proto.read(sys.stdin.buffer, build_event_stream_pb2.BuildEvent):
        msgs.append(msg)
        msg_id = msg.id.WhichOneof('id')
        # print(f'{msg_id=}')
        # XXX: Check for success
        if msg_id == 'test_result':
            label = msg.id.test_result.label
            dt = msg.test_result.test_attempt_duration.ToTimedelta()
            # Accumulate multiple?
            label_to_runtime[label] = dt
            # print(f'{msg=}')
        # if msg_id == 'test_summary':
        #     label = msg.id.test_summary.label
        #     # Divide by run count to get average
        #     dt = (
        #         msg.test_summary.total_run_duration.ToTimedelta() /
        #         msg.test_summary.run_count)
        #     print(label, dt)
        #     # print(f'{msg=}')
        #     label_to_runtime[label] = dt
    table = sorted(label_to_runtime.items(), key=lambda kv: -kv[1])
    print(tabulate.tabulate(table, headers=['Label', 'dt']))

    # print(f'Num Messages: {len(msgs)}')


if __name__ == '__main__':
    main()
