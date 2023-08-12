from evalquiz_pipeline_server.exceptions import (
    PipelineModuleCompositionNotValidException,
)
from evalquiz_pipeline_server.pipeline_module_implementations.internal_pipeline_module import (
    InternalPipelineModule,
)


class Pipeline:
    def __init__(self, reference: str, pipeline_modules: list[InternalPipelineModule]):
        self.reference = reference
        self.pipeline_modules = pipeline_modules
        if (
            not self.validate_io_composition()
            or not self.validate_split_merge_composition()
        ):
            raise PipelineModuleCompositionNotValidException()

    def validate_io_composition(self) -> bool:
        for first, second in zip(self.pipeline_modules, self.pipeline_modules[1:]):
            if first.output_datatype != second.input_datatype:
                return False
        return True

    def validate_split_merge_composition(self) -> bool:
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
