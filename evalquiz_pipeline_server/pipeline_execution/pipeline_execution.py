from typing import Any, Tuple
import ray
from evalquiz_pipeline_server.exceptions import PipelineExecutionSplitValueError
from evalquiz_pipeline_server.pipeline_execution.pipeline import Pipeline
from evalquiz_pipeline_server.pipeline_module_implementations.internal_pipeline_module import (
    InternalPipelineModule,
)

class PipelineExecution:
    def __init__(self, input: Any, pipeline: Pipeline) -> None:
        self.pipeline = pipeline
        self.ray_object_ref = _run.remote(input, self.pipeline)
        
    def run(self) -> Any:    
        return ray.get(self.ray_object_ref)


@ray.remote
def _run(input: Any, pipeline: Pipeline) -> Any:
    try:
        pipeline_module, pipeline = pop_next_pipeline_module(pipeline)
    except KeyError:
        return input
    if not pipeline_module.split and not pipeline_module.merge:
        output = _run_pipeline_module.remote(input, pipeline_module)
        input = _run.remote(output, pipeline)
    if pipeline_module.split:
        _run_pipeline_module_split(input, pipeline_module)
        input = [_run.remote(element, pipeline) for element in input]
    if pipeline_module.merge:
        if not pipeline_module.split:
            input = _run_pipeline_module.remote(input, pipeline_module)
    return input


def pop_next_pipeline_module(
    pipeline: Pipeline,
) -> Tuple[InternalPipelineModule, Pipeline]:
    pipeline_module = pipeline.pipeline_modules[0]
    pipeline_modules = pipeline.pipeline_modules[1:]
    pipeline = Pipeline("intermediate_execution_pipeline", pipeline_modules)
    return pipeline_module, pipeline


def _run_pipeline_module_split(
    input: Any, pipeline_module: InternalPipelineModule
) -> Any:
    if not isinstance(input, list):
        raise PipelineExecutionSplitValueError()
    input = [_run_pipeline_module.remote(element, pipeline_module) for element in input]


@ray.remote
def _run_pipeline_module(input: Any, pipeline_module: InternalPipelineModule) -> Any:
    return pipeline_module.run(input)
