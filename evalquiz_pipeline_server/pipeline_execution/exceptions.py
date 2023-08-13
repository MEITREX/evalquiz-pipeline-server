class PipelineModuleCompositionNotValidException(Exception):
    """Input and output datatypes at least one successive PipelineModule are not compatible."""


class PipelineExecutionException(Exception):
    """Unexpected behavior occurred in the execution of a PipelineModule"""