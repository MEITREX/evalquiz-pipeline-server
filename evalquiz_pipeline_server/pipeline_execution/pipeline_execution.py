from typing import Any, AsyncIterator, Optional
from evalquiz_pipeline_server.pipeline_execution.exceptions import (
    PipelineExecutionException,
)
from evalquiz_pipeline_server.pipeline_execution.pipeline import Pipeline
from evalquiz_proto.shared.generated import (
    BatchStatus,
    ModuleStatus,
    PipelineModule,
    PipelineStatus,
)


class PipelineExecution:
    def __init__(self, input: Any, pipeline: Pipeline) -> None:
        self.pipeline = pipeline
        self.input = input
        first_pipeline_module = self.pipeline.pipeline_modules[0]
        self.pipeline_status = self._build_pipeline_status(
            first_pipeline_module, ModuleStatus.IDLE
        )

    async def run(self) -> AsyncIterator[PipelineStatus]:
        input = self.input
        for pipeline_module in self.pipeline.pipeline_modules:
            yield self._build_pipeline_status(pipeline_module, ModuleStatus.RUNNING)
            try:
                output = pipeline_module.run(input)
            except PipelineExecutionException as e:
                yield self._build_pipeline_status(
                    pipeline_module, ModuleStatus.FAILED, None, str(e)
                )
                return
            input = output
        last_pipeline_module = self.pipeline.pipeline_modules[-1]
        yield self._build_pipeline_status(
            last_pipeline_module, ModuleStatus.SUCCESS, output
        )

    def _build_pipeline_status(
        self,
        pipeline_module: PipelineModule,
        module_status: ModuleStatus,
        result: Optional[Any] = None,
        error_message: Optional[str] = None,
    ) -> PipelineStatus:
        batch_status = BatchStatus(error_message, pipeline_module, module_status)
        return PipelineStatus(result, [batch_status])
