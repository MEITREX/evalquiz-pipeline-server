from evalquiz_proto.shared.exceptions import (
    PipelineModuleCompositionNotValidException,
)
from evalquiz_pipeline_server.pipeline_execution.internal_pipeline_module import (
    InternalPipelineModule,
)


class Pipeline:
    def __init__(self, reference: str, pipeline_modules: list[InternalPipelineModule]):
        """Constructor of Pipeline.

        Args:
            reference (str): Reference of pipeline.
            pipeline_modules (list[InternalPipelineModule]): Implementations of pipeline modules describing the pipeline module execution order.

        Raises:
            PipelineModuleCompositionNotValidException
        """
        self.reference = reference
        self.pipeline_modules = pipeline_modules
        if (
            not self.validate_io_composition()
            or not self.validate_split_merge_composition()
        ):
            raise PipelineModuleCompositionNotValidException()

    def validate_io_composition(self) -> bool:
        """Validates IO compatibility types of successive InternalPipelineModules.

        Returns:
            bool: True, if IO is compatible.
        """
        for first, second in zip(self.pipeline_modules, self.pipeline_modules[1:]):
            if first.output_datatype != second.input_datatype:
                return False
        return True

    def validate_split_merge_composition(self) -> bool:
        """Validates split-merge compatibility of Pipeline.

        Returns:
            bool: True, if split-merge flags are compatible.
        """
        split = False
        merge = False
        for pipeline_module_implementation in self.pipeline_modules:
            if pipeline_module_implementation.split:
                if split:
                    return False
                split = True
                merge = False
            if pipeline_module_implementation.merge:
                if not split or merge:
                    return False
                merge = True
                split = False
        if split:
            return False
        return True
