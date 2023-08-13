from collections import defaultdict
from typing import Any, AsyncIterator
from evalquiz_pipeline_server.pipeline_execution.pipeline import Pipeline
from evalquiz_pipeline_server.pipeline_execution.pipeline_execution import (
    PipelineExecution,
)
from evalquiz_pipeline_server.pipeline_module_implementations.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import BatchStatus, PipelineModule, PipelineStatus


class PipelineExecutor:
    def __init__(
        self,
        pipelines: defaultdict[str, Pipeline] = defaultdict(),
        pipeline_module_implementations: defaultdict[
            str, InternalPipelineModule
        ] = defaultdict(),
    ) -> None:
        self.pipelines: defaultdict[str, Pipeline] = pipelines
        self.pipeline_module_implementations: defaultdict[
            str, InternalPipelineModule
        ] = pipeline_module_implementations

    def add_pipeline(
        self, reference: str, pipeline_modules: list[InternalPipelineModule]
    ) -> None:
        pipeline = Pipeline(reference, pipeline_modules)
        self.pipelines[reference] = pipeline

    def delete_pipeline(self, reference: str) -> None:
        if reference in self.pipelines.keys():
            del self.pipelines[reference]

    def run_pipeline(self, reference: str, input: Any) -> AsyncIterator[PipelineStatus]:
        pipeline = self.pipelines[reference]
        pipeline_execution = PipelineExecution(input, pipeline)
        return pipeline_execution.run()
