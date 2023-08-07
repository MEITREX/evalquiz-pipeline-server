from typing import AsyncIterator
from evalquiz_proto.shared.generated import BatchStatus, PipelineModule, PipelineStatus


class PipelineExecutor:
    async def get_pipeline_status_on_change(
        self, pipeline_thread: str
    ) -> AsyncIterator[PipelineStatus]:
        # This is just for test purposes, # Not Implemented!
        yield PipelineStatus(
            None,
            [BatchStatus(error_message=None, pipeline_module=PipelineModule(value=0))],
        )
