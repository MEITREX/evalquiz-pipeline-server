from typing import Any
from evalquiz_pipeline_server.pipeline_execution.pipeline import Pipeline
from evalquiz_pipeline_server.pipeline_execution.pipeline_execution import (
    PipelineExecution,
)

from evalquiz_pipeline_server.pipeline_module_implementations.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import PipelineModule


class IncInternalPipelineModule(InternalPipelineModule):
    def __init__(self) -> None:
        pipeline_module = PipelineModule("inc", "int", "int")
        super().__init__(pipeline_module)

    def run(self, input: Any) -> Any:
        return input + 1


def test_linear_pipeline_execution() -> None:
    inc_pipeline_module = IncInternalPipelineModule()
    pipeline_modules: list[InternalPipelineModule] = [
        inc_pipeline_module,
        inc_pipeline_module,
        inc_pipeline_module,
    ]
    pipeline = Pipeline("test_pipeline", pipeline_modules)
    pipeline_execution = PipelineExecution(0, pipeline)
    result = pipeline_execution.run()
    print(result)
    assert result == 3
