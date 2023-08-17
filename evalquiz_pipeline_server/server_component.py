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
        pipeline_status_iterator = self.pipeline_executor.run_pipeline(
            "evalquiz_config_iteration", internal_config
        )
        while True:
            try:
                pipeline_status = await pipeline_status_iterator.__anext__()
                yield pipeline_status
            except StopAsyncIteration:
                break
