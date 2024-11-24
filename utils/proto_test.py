import io
import unittest

from examples.basic import hello_pb2
from utils import proto


class TestProtoDelimited(unittest.TestCase):
    def test_basics(self) -> None:
        buf = io.BytesIO()
        msg = hello_pb2.Hello(id=12345)
        proto.write(buf, msg)
        msg2 = hello_pb2.Hello(id=6789)
        proto.write(buf, msg2)
        # XXX: Validate bytes themselves
        expected_bytes = bytes([
            # 3 bytes: field + varint
            0x03, 0x08, 0xB9, 0x60,
            # MSG 2
            0x03, 0x08, 0x85, 0x35])
        # b'\x03\x08\xb9`\x03\x08\x855'
        self.assertEqual(expected_bytes, buf.getvalue())

        # Read from the same thing
        buf.seek(0)
        expected_msgs = [msg, msg2]
        while r_msg := proto.read(buf, hello_pb2.Hello):
            expected_msg = expected_msgs.pop(0)
            self.assertEqual(r_msg, expected_msg)
        self.assertFalse(expected_msgs)
