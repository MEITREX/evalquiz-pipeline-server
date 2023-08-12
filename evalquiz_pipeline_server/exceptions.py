class PipelineModuleCompositionNotValidException(Exception):
    """Input and output datatypes at least one successive PipelineModule are not compatible."""


class PipelineExecutionSplitValueError(ValueError):
    """The input of a split node must be of type list[Any]."""
