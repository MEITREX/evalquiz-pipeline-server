from typing import Any, Optional, cast
from evalquiz_pipeline_server.pipeline_execution.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import (
    InternalConfig,
    PipelineModule,
    GenerationResult,
)


class QuestionSpecificationMerge(InternalPipelineModule):
    def __init__(self) -> None:
        pipeline_module = PipelineModule(
            "question_specification_merge",
            "tuple[InternalConfig, list[Optional[GenerationResult]]]",
            "InternalConfig",
        )
        super().__init__(pipeline_module)

    async def run(self, input: Any) -> Any:
        raise NotImplementedError()
