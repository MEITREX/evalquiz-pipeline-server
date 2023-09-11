import betterproto
from evalquiz_proto.shared.generated import EvaluationResult


class EvaluationResultTemplate:
    def result_template(self, evaluation_result: EvaluationResult) -> str:
        (_, result_value) = betterproto.which_one_of(
            evaluation_result, "evaluation_result"
        )
        if result_value is None:
            raise ValueError(
                "EvaluationResult is not set. EvaluationResult template cannot be built."
            )
        return "<result type=evaluation>" + str(result_value) + "</result>\n\n"
