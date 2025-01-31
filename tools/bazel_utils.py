"""Tools for working with bazel.

XXX: Should --notool_deps be specified?

Should we denote source files in some way? eg)
- bazel query 'labels(srcs, //...) union labels(hdrs, //...)'

```
bazel query //... --output proto > query_result.pb
# Load then operate on it
# For example
bazel query //... --output=proto |tee result.pb |bazel run //apps:bazel_parser
```
"""

from third_party.bazel.src.main.protobuf import build_pb2


def parse_build_output(query_bytes: bytes) -> build_pb2.QueryResult:
    result = build_pb2.QueryResult()
    result.ParseFromString(query_bytes)
    return result
