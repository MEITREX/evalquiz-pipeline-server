import asyncio
from grpclib.server import Server
from evalquiz_pipeline_server.evalquiz_config_iteration.pipelines.config_iteration_pipeline import (
    ConfigIterationPipeline,
)
from evalquiz_pipeline_server.pipeline_execution.pipeline_executor import (
    PipelineExecutor,
)
from evalquiz_proto.shared.generated import (
    InternalConfig,
    PipelineServerBase,
    PipelineStatus,
)

from typing import AsyncIterator


class PipelineServerService(PipelineServerBase):
    """Serves endpoints for Evalquiz config iteration."""

    def __init__(self) -> None:
        """Constructor of PipelineServerService."""
        self.pipeline_executor = PipelineExecutor()
        self.pipeline_executor.pipelines[
            "evalquiz_config_iteration"
        ] = ConfigIterationPipeline()

    async def iterate_config(
        self, internal_config: InternalConfig
    ) -> "AsyncIterator[PipelineStatus]":
        """Asynchronous method that is used by gRPC as an endpoint.
        Iterates an Evalquiz config by running the `evalquiz_config_iteration` pipeline on the `internal_config` input.

        Args:
            internal_config (InternalConfig): Evalquiz config to iterate.

        Returns:
            AsyncIterator[PipelineStatus]: An iterator which elements represent the current status of the config iteration.
        """
        print(internal_config, flush=True)
        pipeline_status_iterator = self.pipeline_executor.run_pipeline(
            "evalquiz_config_iteration", internal_config
        )
        while True:
            try:
                pipeline_status = await pipeline_status_iterator.__anext__()
                yield pipeline_status
            except StopAsyncIteration:
                break


async def main() -> None:
    server = Server([PipelineServerService()])
    await server.start("0.0.0.0", 50051)
    print("Server started at port 50051.", flush=True)
    await server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
