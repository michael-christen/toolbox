import unittest

from examples.basic import hello_pb2


class TestHello(unittest.TestCase):
    """Test proto loading."""

    def test_basics(self):
        msg = hello_pb2.Hello(id=4)
        self.assertEqual(msg.id, 4)
