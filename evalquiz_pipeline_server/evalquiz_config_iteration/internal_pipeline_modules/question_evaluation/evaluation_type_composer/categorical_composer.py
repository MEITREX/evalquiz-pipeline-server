import betterproto
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.evaluation_type_composer.evaluation_result_template import (
    EvaluationResultTemplate,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.evaluation_type_composer.evaluation_result_type_composer import (
    EvaluationResultTypeComposer,
)
from evalquiz_proto.shared.generated import (
    Categorical,
    EvaluationResult,
    EvaluationResultType,
)


class CategoricalComposer(EvaluationResultTypeComposer, EvaluationResultTemplate):
    def __init__(self) -> None:
        super().__init__(
            "categorical",
            EvaluationResult(str_value="CATEGORY"),
        )

    def compose_query_message(
        self, evaluation_result_type: EvaluationResultType
    ) -> str:
        (_, categorical) = betterproto.which_one_of(
            evaluation_result_type, "evaluation_result_type"
        )
        if categorical is None or not isinstance(categorical, Categorical):
            raise ValueError("Categorical was not instantiated correctly.")
        query_message = (
            self.result_template()
            + "Where CATEGORY is one of the following categories:\n"
        )
        for category in categorical.categories:
            query_message += category + "\n"
        query_message += "\n"
        return query_message
