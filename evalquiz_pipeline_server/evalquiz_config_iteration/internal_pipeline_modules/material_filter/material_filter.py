from typing import Any
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.material_client import (
    MaterialClient,
)
from evalquiz_pipeline_server.pipeline_execution.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import InternalConfig, PipelineModule


class MaterialFilter(InternalPipelineModule):
    def __init__(self) -> None:
        pipeline_module = PipelineModule(
            "material_filter", "InternalConfig", "Tuple[InternalConfig, str]"
        )
        super().__init__(pipeline_module)
        self.material_client = MaterialClient()

    async def run(self, input: Any) -> Any:
        if not isinstance(input, InternalConfig):
            raise TypeError()
        self.material_client = MaterialClient(input.material_server_urls)
