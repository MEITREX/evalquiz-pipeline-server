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
    """Test InternalPipelineModule that increments an integer value."""

    def __init__(self) -> None:
        """Constructor of IncInternalPipelineModule."""
        pipeline_module = PipelineModule("inc", "int", "int")
        super().__init__(pipeline_module)

    async def run(self, input: Any) -> Any:
        """Incrementation function.

        Args:
            input (Any): Integer value

        Returns:
            Any: Integer value incremented by 1.
        """
        return input + 1


@pytest.mark.asyncio
async def test_linear_pipeline_execution() -> None:
    """Tests execution of a Pipeline with 3 IncInternalPipelineModule instances."""
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
