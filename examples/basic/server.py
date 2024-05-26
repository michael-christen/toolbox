import asyncio
import logging

import grpc

from examples.basic import hello_pb2
from examples.basic import hello_pb2_grpc


class Greeter(hello_pb2_grpc.GreeterServicer):
    async def SayHello(
        self,
        request: hello_pb2.HelloRequest,
        context: grpc.aio.ServicerContext,
    ) -> hello_pb2.HelloReply:
        return hello_pb2.HelloReply(message="Hello, %s!" % request.name)


def get_server() -> grpc.aio.server:
    server = grpc.aio.server()
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    return server


async def serve() -> None:
    server = get_server()
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
