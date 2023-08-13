from abc import abstractmethod
from typing import Any
from evalquiz_proto.shared.generated import PipelineModule


class InternalPipelineModule(PipelineModule):
    def __init__(
        self,
        pipeline_module: PipelineModule,
        split: bool = False,
        merge: bool = False,
    ):
        self.name = pipeline_module.name
        self.input_datatype = pipeline_module.input_datatype
        self.output_datatype = pipeline_module.output_datatype
        self.split = split
        self.merge = merge

    @abstractmethod
    def run(self, input: Any) -> Any:
        pass
