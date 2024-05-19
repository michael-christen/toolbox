import asyncio
import unittest

from examples.basic import hello_pb2
from examples.basic import client
from examples.basic import server


class TestHello(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.s = server.get_server()
        await self.s.start()

    async def asyncTearDown(self):
        await self.s.stop(grace=None)
        await self.s.wait_for_termination()

    async def test_basics(self):
        result = await client.get_response()
        self.assertEqual(
            hello_pb2.HelloReply(message='Hello, you!'),
            result)


if __name__ == '__main__':
    # XXX: Automate this
    unittest.main()