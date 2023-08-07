from evalquiz_pipeline_server.pipeline_execution.pipeline_executor import PipelineExecutor
from evalquiz_proto.shared.generated import (
    InternalConfig,
    PipelineServerBase,
    PipelineStatus,
)
from grpclib.server import Server
from typing import AsyncIterator

class PipelineServerService(PipelineServerBase):
    """Serves endpoints for material manipulation."""

    def __init__(self) -> None:
        self.pipeline_executor = PipelineExecutor()

    async def iterate_config(self, internal_config: InternalConfig) -> "AsyncIterator[PipelineStatus]":
        pipeline_thread = "Test hash!"
        pipeline_status_iterator = (
            self.pipeline_executor.get_pipeline_status_on_change(pipeline_thread)
        )
        while True:
            try:
                pipeline_status = await pipeline_status_iterator.__anext__()
                yield pipeline_status
            except StopAsyncIteration:
                break