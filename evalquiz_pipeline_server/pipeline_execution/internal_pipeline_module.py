from abc import ABC, abstractmethod
from typing import Any
from evalquiz_proto.shared.generated import PipelineModule


class InternalPipelineModule(PipelineModule, ABC):
    """An implementation of a PipelineModule."""

    def __init__(
        self,
        pipeline_module: PipelineModule,
        split: bool = False,
        merge: bool = False,
    ):
        """Constructor of InternalPipelineModule.

        Args:
            pipeline_module (PipelineModule): PipelineModule that the implementation is written for.
            split (bool, optional): If the implementation returns multiple threads for the next InternalPipelineModule. Defaults to False.
            merge (bool, optional): If the implementation supports multiple threads as an input and collects them into one resulting thread. Defaults to False.
        """
        self.name = pipeline_module.name
        self.input_datatype = pipeline_module.input_datatype
        self.output_datatype = pipeline_module.output_datatype
        self.split = split
        self.merge = merge

    @abstractmethod
    async def run(self, input: Any) -> Any:
        """The execution logic of the pipeline module.
        Checks IO-types on runtime.

        Args:
            input (Any): Input to pipeline implementation.

        Returns:
            Any: Output of pipeline implementation.
        """
        pass

    def cast_to_pipeline_module(self) -> PipelineModule:
        """Casts self object to object of superclass: PipelineModule.
        This method is required, as Python does not feature object type casting.

        Returns:
            PipelineModule: Self object casted into PipelineModule.
        """
        return PipelineModule(self.name, self.input_datatype, self.output_datatype)
