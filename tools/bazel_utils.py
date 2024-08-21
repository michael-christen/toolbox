"""Tools for working with bazel.

```
bazel query //... --output proto > query_result.pb
# Load then operate on it
# For example
bazel query //... --output=proto |tee result.pb |bazel run //apps:bazel_parser
```
"""

from third_party.bazel.src.main.protobuf import build_pb2
from third_party.bazel.src.main.java.com.google.devtools.build.lib.buildeventstream.proto import build_event_stream_pb2


def parse_build_output(query_bytes: bytes) -> build_pb2.QueryResult:
    result = build_pb2.QueryResult()
    result.ParseFromString(query_bytes)
    return result


def parse_build_event(build_event_bytes: bytes
                      ) -> build_event_stream_pb2.BuildEvent:
    result = build_event_stream_pb2.BuildEvent()
    result.ParseFromString(build_event_bytes)
    return result

