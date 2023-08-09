from collections import defaultdict
from typing import Any, AsyncIterator
from evalquiz_pipeline_server.pipeline_execution.pipeline import Pipeline
from evalquiz_pipeline_server.pipeline_module_implementations.pipeline_module_implementation import (
    PipelineModuleImplementation,
)
from evalquiz_proto.shared.generated import BatchStatus, PipelineModule, PipelineStatus


class PipelineExecutor:
    def __init__(
        self,
        pipelines: defaultdict[str, Pipeline] = defaultdict(),
        pipeline_module_implementations: defaultdict[
            str, PipelineModuleImplementation
        ] = defaultdict(),
    ) -> None:
        self.pipelines: defaultdict[str, Pipeline] = pipelines
        self.pipeline_module_implementations: defaultdict[
            str, PipelineModuleImplementation
        ] = pipeline_module_implementations

    def add_pipeline(
        self, reference: str, pipeline_modules: list[PipelineModule]
    ) -> None:
        pipeline = Pipeline(reference, pipeline_modules)
        self.pipelines[reference] = pipeline

    def delete_pipeline(self, reference: str) -> None:
        if reference in self.pipelines.keys():
            del self.pipelines[reference]

    async def run_pipeline(self, reference: str, input: Any) -> str:
        raise NotImplementedError()

    def validate_implementation_for_pipeline(self, pipeline_reference: str) -> bool:
        split = False
        merge = False
        pipeline = self.pipelines[pipeline_reference]
        for pipeline_module in pipeline.pipeline_modules:
            pipeline_module_implementation = self.pipeline_module_implementations[
                pipeline_module.name
            ]
            if pipeline_module_implementation.split:
                if split:
                    return False
                split = True
                merge = False
            if pipeline_module_implementation.merge:
                if not split or merge:
                    return False
                merge = True
                split = False
        if split:
            return False
        return True

    async def get_pipeline_status_on_change(
        self, pipeline_thread: str
    ) -> AsyncIterator[PipelineStatus]:
        # This is just for test purposes, # Not Implemented!
        yield PipelineStatus(
            None,
            [
                BatchStatus(
                    error_message=None, pipeline_module=PipelineModule("", "", "")
                )
            ],
        )
