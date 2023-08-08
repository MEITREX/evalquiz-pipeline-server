from collections import defaultdict
from typing import Any, AsyncIterator
from evalquiz_pipeline_server.pipeline_execution.pipeline import Pipeline
from evalquiz_pipeline_server.pipeline_module_implementations.pipeline_module_implementation import PipelineModuleImplementation
from evalquiz_proto.shared.generated import BatchStatus, PipelineModule, PipelineStatus

class PipelineExecutor:

    def __init__(self, pipelines: defaultdict[str, Pipeline] = defaultdict(), pipeline_module_implementations: defaultdict[str, PipelineModuleImplementation] = defaultdict()) -> None:
        self.pipelines: defaultdict[str, Pipeline] = pipelines
        self.pipeline_module_implementations: dict[str, PipelineModuleImplementation] = pipeline_module_implementations

    def add_pipeline(self, reference: str, pipeline_modules: list[PipelineModule]) -> None:
        pipeline = Pipeline(reference, pipeline_modules)
        self.pipelines[reference] = pipeline

    def delete_pipeline(self, reference: str) -> None:
        if reference in self.pipelines.keys():
            del self.pipelines[reference]

    async def run_pipeline(self, reference: str, input: Any) -> str:
        raise NotImplementedError()

    async def get_pipeline_status_on_change(
        self, pipeline_thread: str
    ) -> AsyncIterator[PipelineStatus]:
        # This is just for test purposes, # Not Implemented!
        yield PipelineStatus(
            None,
            [BatchStatus(error_message=None, pipeline_module=PipelineModule("", "", ""))],
        )
