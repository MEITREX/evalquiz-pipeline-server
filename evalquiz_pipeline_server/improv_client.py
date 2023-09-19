import asyncio
from grpclib.client import Channel
from evalquiz_proto.shared.generated import InternalConfig, PipelineServerStub


async def main() -> None:
    channel = Channel(host="0.0.0.0", port=50051)
    service = PipelineServerStub(channel)
    async for response in service.iterate_config(InternalConfig()):
        print(response)

    # don't forget to close the channel when done!
    channel.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
