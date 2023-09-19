import betterproto
from evalquiz_proto.shared.generated import GenerationResult


class GenerationResultTemplate:
    def result_template(self, generation_result: GenerationResult) -> str:
        (_, result_value) = betterproto.which_one_of(
            generation_result, "generation_result"
        )
        if result_value is None:
            raise ValueError(
                "GenerationResult is not set. GenerationResult template cannot be built."
            )
        json_result = result_value.to_json(indent=4, include_default_values=True)
        return "<result type=generation>" + json_result + "</result>\n\n"
