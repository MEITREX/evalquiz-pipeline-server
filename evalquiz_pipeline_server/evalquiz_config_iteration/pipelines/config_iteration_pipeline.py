from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.material_filter import (
    MaterialFilter,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_drop import (
    QuestionDrop,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation import (
    QuestionEvaluation,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation import (
    QuestionGeneration,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_specification_merge import (
    QuestionSpecificationMerge,
)
from evalquiz_pipeline_server.pipeline_execution.pipeline import Pipeline


class ConfigIterationPipeline(Pipeline):
    """Evalquiz config iteration pipeline."""

    def __init__(self) -> None:
        """Constructor of ConfigIterationPipeline."""
        pipeline_modules = [
            MaterialFilter(),
            QuestionGeneration(),
            QuestionSpecificationMerge(),
            QuestionEvaluation(),
            QuestionDrop(),
        ]
        super().__init__("config_iteration_pipeline", pipeline_modules)