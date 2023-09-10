import betterproto
from evalquiz_proto.shared.generated import EvaluationResult


class EvaluationResultTemplate:
    def result_template(self, evaluation_result: EvaluationResult) -> str:
        (_, result_value) = betterproto.which_one_of(
            evaluation_result, "evaluation_result"
        )
        if result_value is None:
            raise ValueError(
                "EvaluationResult is not set. GenerationResult template cannot be built."
            )
        json_result = result_value.to_json(indent=4)
        return "<result>\n" + json_result + "\n</result>\n\n"
