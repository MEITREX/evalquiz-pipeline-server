from typing import Any
from evalquiz_pipeline_server.pipeline_execution.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import PipelineModule


class MaterialFilter(InternalPipelineModule):
    def __init__(self) -> None:
        pipeline_module = PipelineModule(
            "material_filter", "InternalConfig", "Tuple[InternalConfig, str]"
        )
        super().__init__(pipeline_module)

    def run(self, input: Any) -> Any:
        raise NotImplementedError()
