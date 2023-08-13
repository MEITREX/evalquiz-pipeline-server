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
    """Serves endpoints for material manipulation."""

    def __init__(self) -> None:
        self.pipeline_executor = PipelineExecutor()

    async def iterate_config(
        self, internal_config: InternalConfig
    ) -> "AsyncIterator[PipelineStatus]":
        pipeline_status_iterator = self.pipeline_executor.run_pipeline(
            "evalquiz_config_iteration", internal_config
        )
        while True:
            try:
                pipeline_status = await pipeline_status_iterator.__anext__()
                yield pipeline_status
            except StopAsyncIteration:
                break
