import asyncio
import logging

import grpc

from third_party.bazel.proto import build_event_stream_pb2
from third_party.bazel.proto import publish_build_event_pb2
from third_party.bazel.proto import publish_build_event_pb2_grpc


class BesServicer(publish_build_event_pb2_grpc.PublishBuildEventServicer):
    async def PublishLifecycleEvent(
        self,
        request: publish_build_event_pb2.PublishLifecycleEventRequest,
        context: grpc.aio.ServicerContext,
    ) -> Empty:
        ...

    async def PublishBuildToolEventSream(
        self,
        request: publish_build_event_pb2.PublishLifecycleEventRequest,
        context: grpc.aio.ServicerContext,
    ) -> Empty:
        ...




def get_server() -> grpc.aio.Server:
    server = grpc.aio.server()
    publish_build_event_pb2_grpc.add_XServicer_to_server(BesServicer(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    return server


async def serve() -> None:
    server = get_server()
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
