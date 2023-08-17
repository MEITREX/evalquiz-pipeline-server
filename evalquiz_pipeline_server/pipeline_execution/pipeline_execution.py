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
        """Constructor of PipelineExecution.

        Args:
            input (Any): Input of execution.
            pipeline (Pipeline): Pipeline that should be executed.
        """
        self.pipeline = pipeline
        self.input = input
        first_pipeline_module = self.pipeline.pipeline_modules[0]
        self.pipeline_status = self._build_pipeline_status(
            first_pipeline_module, ModuleStatus.IDLE
        )

    async def run(self) -> AsyncIterator[PipelineStatus]:
        """Execution logic that chains InternalPipelineModules together and executes their run() method.

        Returns:
            AsyncIterator[PipelineStatus]: Iterator with PipelineStatus of the current execution.
        """
        input = self.input
        for pipeline_module in self.pipeline.pipeline_modules:
            yield self._build_pipeline_status(pipeline_module, ModuleStatus.RUNNING)
            try:
                output = await pipeline_module.run(input)
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
        """Helper method to build PipelineStatus according to method parameters.

        Args:
            pipeline_module (PipelineModule): PipelineModule of status.
            module_status (ModuleStatus): Module status itself.
            result (Optional[Any], optional): Result of the last pipeline execution step. Defaults to None.
            error_message (Optional[str], optional): An error that occurred while executing the given PipelineModule. Defaults to None.

        Returns:
            PipelineStatus: The built PipelineStatus.
        """
        batch_status = BatchStatus(error_message, pipeline_module, module_status)
        return PipelineStatus(result, [batch_status])
