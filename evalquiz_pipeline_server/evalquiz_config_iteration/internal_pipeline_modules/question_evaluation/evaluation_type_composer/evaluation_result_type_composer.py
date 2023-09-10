from abc import ABC, abstractmethod
from typing import Optional

import betterproto
from evalquiz_proto.shared.generated import EvaluationResult, EvaluationResultType


class EvaluationResultTypeComposer(ABC):
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
        (_, result_value) = betterproto.which_one_of(
            evaluation_result, "evaluation_result"
        )
        if result_value is None:
            raise ValueError(
                "EvaluationResult is not set. EvaluationResult template cannot be built."
            )
        json_result = result_value.to_json(indent=4)
        return "<result>\n" + json_result + "\n</result>\n\n"
