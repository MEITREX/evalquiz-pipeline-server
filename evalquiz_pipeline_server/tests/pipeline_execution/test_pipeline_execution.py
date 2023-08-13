from typing import Any
from evalquiz_pipeline_server.pipeline_execution.pipeline import Pipeline
from evalquiz_pipeline_server.pipeline_execution.pipeline_execution import (
    PipelineExecution,
)
import pytest

from evalquiz_pipeline_server.pipeline_execution.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import ModuleStatus, PipelineModule


class IncInternalPipelineModule(InternalPipelineModule):
    def __init__(self) -> None:
        pipeline_module = PipelineModule("inc", "int", "int")
        super().__init__(pipeline_module)

    def run(self, input: Any) -> Any:
        return input + 1


@pytest.mark.asyncio
async def test_linear_pipeline_execution() -> None:
    inc_pipeline_module = IncInternalPipelineModule()
    pipeline_modules: list[InternalPipelineModule] = [
        inc_pipeline_module,
        inc_pipeline_module,
        inc_pipeline_module,
    ]
    pipeline = Pipeline("test_pipeline", pipeline_modules)
    pipeline_execution = PipelineExecution(0, pipeline)
    pipeline_status_iterator = pipeline_execution.run()
    while True:
        try:
            pipeline_status = await pipeline_status_iterator.__anext__()
        except StopAsyncIteration:
            break
    assert pipeline_status.batch_status[0].module_status == ModuleStatus.SUCCESS
    assert pipeline_status.result == 3
