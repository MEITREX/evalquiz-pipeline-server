from collections import defaultdict
from typing import Any, AsyncIterator
from evalquiz_pipeline_server.pipeline_execution.pipeline import Pipeline
from evalquiz_pipeline_server.pipeline_execution.pipeline_execution import (
    PipelineExecution,
)
from evalquiz_pipeline_server.pipeline_execution.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import PipelineStatus


class PipelineExecutor:
    def __init__(
        self,
        pipelines: defaultdict[str, Pipeline] = defaultdict(),
    ) -> None:
        """Constructor of PipelineExecutor.

        Args:
            pipelines (defaultdict[str, Pipeline], optional): Available pipelines to execute. Defaults to defaultdict().
        """
        self.pipelines: defaultdict[str, Pipeline] = pipelines

    def add_pipeline(
        self, reference: str, pipeline_modules: list[InternalPipelineModule]
    ) -> None:
        """Adds a pipeline to self.pipelines

        Args:
            reference (str): Reference that the pipeline can be accessed under.
            pipeline_modules (list[InternalPipelineModule]): Implementations of pipeline modules describing the pipeline module execution order.
        """
        pipeline = Pipeline(reference, pipeline_modules)
        self.pipelines[reference] = pipeline

    def delete_pipeline(self, reference: str) -> None:
        """Deletes a pipeline from self.pipelines

        Args:
            reference (str): Reference of pipeline that should be deleted.
        """
        if reference in self.pipelines.keys():
            del self.pipelines[reference]

    def run_pipeline(self, reference: str, input: Any) -> AsyncIterator[PipelineStatus]:
        """Creates and runs a new PipelineExecution on specified pipeline.

        Args:
            reference (str): Reference of pipeline that should be executed.
            input (Any): Input of PipelineExecution.

        Returns:
            AsyncIterator[PipelineStatus]: Iterator with PipelineStatus of the current execution.
        """
        pipeline = self.pipelines[reference]
        pipeline_execution = PipelineExecution(input, pipeline)
        return pipeline_execution.run()
