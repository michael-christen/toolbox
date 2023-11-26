import unittest

from experiments.proto.hello import hello_pb2


class TestHello(unittest.TestCase):
    def test_basics(self):
        msg = hello_pb2.Hello(id=4)
        self.fail(str(msg))
