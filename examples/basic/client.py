import asyncio
import logging

import grpc

from examples.basic import hello_pb2
from examples.basic import hello_pb2_grpc


async def get_response() -> hello_pb2.HelloReply:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        return await stub.SayHello(hello_pb2.HelloRequest(name="you"))

async def run() -> None:
    resp = await get_response()
    print("Greeter client received: " + response.message)


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())