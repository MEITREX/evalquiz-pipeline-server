from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.evaluation_implementations.evaluation_implementation import (
    EvaluationImplementation,
)
from evalquiz_proto.shared.generated import EvaluationType, LanguageModelEvaluation


class LanguageModelEvaluationImplementation(EvaluationImplementation):
    def __init__(self) -> None:
        evaluation_type = EvaluationType(
            language_model_evaluation=LanguageModelEvaluation()
        )
        super().__init__(evaluation_type)
