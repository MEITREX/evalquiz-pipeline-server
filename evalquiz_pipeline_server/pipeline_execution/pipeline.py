

from evalquiz_pipeline_server.exceptions import PipelineModuleCompositionNotValidException
from evalquiz_proto.shared.generated import PipelineModule


class Pipeline:

    def __init__(self, reference: str, pipeline_modules: list[PipelineModule]):
        self.reference = reference
        self.pipeline_modules = pipeline_modules
        if not self.validate():
            raise PipelineModuleCompositionNotValidException()
    
    def validate(self) -> bool:
        for first, second in zip(self.pipeline_modules, self.pipeline_modules[1:]):
            if first.input_datatype != second.output_datatype:
                return False
        return True