from abc import abstractmethod
from typing import Any
from evalquiz_proto.shared.generated import PipelineModule


class PipelineModuleImplementation:
    def __init__(
        self,
        pipeline_module: PipelineModule,
        split: bool = False,
        merge: bool = False,
    ):
        self.pipeline_module = pipeline_module
        self.split = split
        self.merge = merge

    @abstractmethod
    def run(input: Any) -> Any:
        pass
