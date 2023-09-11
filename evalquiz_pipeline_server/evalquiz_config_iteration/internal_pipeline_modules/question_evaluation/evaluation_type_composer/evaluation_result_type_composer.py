from abc import ABC, abstractmethod
from typing import Optional

from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.evaluation_type_composer.evaluation_result_template import (
    EvaluationResultTemplate,
)
from evalquiz_proto.shared.generated import EvaluationResult, EvaluationResultType


class EvaluationResultTypeComposer(ABC, EvaluationResultTemplate):
    """Specific instructions to give according to a EvaluationResultType."""

    def __init__(
        self,
        evaluation_result_type: str,
        evaluation_result: EvaluationResult,
    ):
        self.evaluation_result_type = evaluation_result_type
        self.evaluation_result = evaluation_result

    @abstractmethod
    def compose_query_message(
        self, evaluation_result_type: EvaluationResultType
    ) -> str:
        pass

    def result_template(
        self, evaluation_result: Optional[EvaluationResult] = None
    ) -> str:
        evaluation_result = evaluation_result or self.evaluation_result
        return super().result_template(evaluation_result)
