import unittest

from examples.basic import client
from examples.basic import hello_pb2
from examples.basic import server


class TestHello(unittest.IsolatedAsyncioTestCase):
    """Test asyncio client and server with gRPC."""

    async def asyncSetUp(self):
        self.server = server.get_server()
        await self.server.start()

    # Why does coverage not see wait_for_termination as ran?
    async def asyncTearDown(self):  # pragma: no cover
        await self.server.stop(grace=None)
        await self.server.wait_for_termination()

    async def test_basics(self):
        result = await client.get_response()
        self.assertEqual(hello_pb2.HelloReply(message="Hello, you!"), result)
