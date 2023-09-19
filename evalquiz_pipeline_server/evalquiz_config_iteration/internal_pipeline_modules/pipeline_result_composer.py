from typing import Any
from evalquiz_pipeline_server.pipeline_execution.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.exceptions import PipelineModuleRuntimeInputException
from evalquiz_proto.shared.generated import (
    InternalConfig,
    PipelineModule,
    PipelineResult,
)


class PipelineResultComposer(InternalPipelineModule):
    def __init__(self) -> None:
        pipeline_module = PipelineModule(
            "pipeline_result_composer", "InternalConfig", "PipelineResult"
        )
        super().__init__(pipeline_module)

    async def run(self, input: Any) -> Any:
        if not isinstance(input, InternalConfig):
            raise PipelineModuleRuntimeInputException()
        return PipelineResult(internal_config=input)
