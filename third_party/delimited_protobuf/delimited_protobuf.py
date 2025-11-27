"""A set of protobuf related utilities.

Delimited Utilities: handle length-delimited protobuf messages.
- Originally sourced from
https://github.com/soulmachine/delimited-protobuf/blob/main/delimited_protobuf.py
- read/write_delimited
- Similar to:
  - CodedInputStream
  https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/io/coded_stream.h#L66
  - `parseDelimitedFrom()`
  https://github.com/protocolbuffers/protobuf/blob/master/java/core/src/main/java/com/google/protobuf/Parser.java
- Similar to:
  - `CodedOutputStream`
  https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/io/coded_stream.h#L47)
  - `MessageLite#writeDelimitedTo`
  https://github.com/protocolbuffers/protobuf/blob/master/java/core/src/main/java/com/google/protobuf/MessageLite.java#L126
"""

from typing import BinaryIO
from typing import Optional
from typing import Type
from typing import TypeVar

from google.protobuf import message

# NOTE: We use some internal mechanisms here for varint encoding, if we note
# this as being an issue in the future, we can implement our own.
from google.protobuf.internal import decoder
from google.protobuf.internal import encoder

T = TypeVar("T", bound=message.Message)


def _read_varint(stream: BinaryIO) -> int:
    """Read a varint from the stream."""
    buf: bytes = stream.read(1)
    if buf == b"":
        return 0  # reached EOF
    while buf[-1] & 0x80:  # while the MSB is 1
        new_byte = stream.read(1)
        if new_byte == b"":
            raise EOFError("unexpected EOF")
        buf += new_byte
    # XXX: Unclear why these types are invalid
    varint, _ = decoder._DecodeVarint(buf, 0)  # type:ignore
    return varint


def read_delimited(stream: BinaryIO, proto_cls: Type[T]) -> Optional[T]:
    """Read a single length-delimited message from the given stream."""
    size = _read_varint(stream)
    if size == 0:
        return None
    buf = stream.read(size)
    msg = proto_cls()
    msg.ParseFromString(buf)
    return msg


def write_delimited(stream: BinaryIO, msg: T):
    """Write a single length-delimited message to the given stream."""
    # XXX: Unclear why these types are invalid, @pip//protobuf is the culprit,
    # but why?
    encoder._EncodeVarint(stream.write, msg.ByteSize())  # type:ignore
    stream.write(msg.SerializeToString())
