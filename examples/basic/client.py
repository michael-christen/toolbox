import asyncio
import logging

import grpc

from examples.basic import hello_pb2
from examples.basic import hello_pb2_grpc
from third_party.bazel.googleapis.google.devtools.build.v1 import publish_build_event_pb2


async def get_response() -> hello_pb2.HelloReply:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        return await stub.SayHello(hello_pb2.HelloRequest(name="you"))


async def run() -> None:  # pragma: no cover
    resp = await get_response()
    print("Greeter client received: " + resp.message)


if __name__ == "__main__":  # pragma: no cover
    msg = publish_build_event_pb2.PublishBuildToolEventStreamRequest()
    logging.basicConfig()
    asyncio.run(run())
