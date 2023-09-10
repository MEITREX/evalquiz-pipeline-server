import betterproto
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.evaluation_type_composer.evaluation_result_template import (
    EvaluationResultTemplate,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.evaluation_type_composer.evaluation_result_type_composer import (
    EvaluationResultTypeComposer,
)
from evalquiz_proto.shared.generated import (
    ValueRange,
    EvaluationResult,
    EvaluationResultType,
)


class ValueRangeComposer(EvaluationResultTypeComposer, EvaluationResultTemplate):
    def __init__(self) -> None:
        super().__init__(
            "value_range",
            EvaluationResult(float_value=12.34),
        )

    def compose_query_message(
        self, evaluation_result_type: EvaluationResultType
    ) -> str:
        (_, value_range) = betterproto.which_one_of(
            evaluation_result_type, "evaluation_result_type"
        )
        if value_range is None or not isinstance(value_range, ValueRange):
            raise ValueError("Categorical was not instantiated correctly.")
        query_message = (
            self.result_template()
            + "Where 12.34 is a placeholder for a floating point value in range of: ("
            + str(value_range.lower_bound)
            + ", "
            + str(value_range.upper_bound)
            + "), both included."
        )
        return query_message
