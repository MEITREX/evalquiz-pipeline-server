import re
import betterproto
from evalquiz_pipeline_server.evalquiz_config_iteration.api_client_registry import (
    APIClientRegistry,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.internal_evaluations.internal_evaluation import (
    InternalEvaluation,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.result_exceptions import (
    ResultSectionNotFoundException,
)
from evalquiz_proto.shared.generated import (
    Evaluation,
    EvaluationResult,
    LanguageModelEvaluation,
)


class InternalLanguageModelEvaluation(InternalEvaluation):
    def __init__(self) -> None:
        evaluation_type = "language_model_evaluation"
        super().__init__(evaluation_type)
        self.api_client_registry = APIClientRegistry()

    def evaluate(self, evaluation: Evaluation) -> EvaluationResult:
        (_, language_model_evaluation) = betterproto.which_one_of(
            evaluation, "evaluation"
        )
        if language_model_evaluation is None or not isinstance(
            language_model_evaluation, LanguageModelEvaluation
        ):
            raise TypeError("Evaluation is not LanguageModelEvaluation.")
        llm_client = self.api_client_registry.llm_clients[
            language_model_evaluation.model
        ]
        messages = self.compose_messages(language_model_evaluation)
        result_text = llm_client.request_result_text(messages)
        return self.parse_result(result_text)

    def compose_messages(
        self, language_model_evaluation: LanguageModelEvaluation
    ) -> list[dict[str, str]]:
        return (
            [self.compose_system_message()]
            + self.compose_few_shot_examples()
            + [self.compose_query_message()]
        )

    def compose_system_message(self) -> dict[str, str]:
        return {
            "role": "system",
            "content": """
""",
        }

    def compose_few_shot_examples(self) -> list[dict[str, str]]:
        raise NotImplementedError()

    def compose_query_message(self) -> dict[str, str]:
        raise NotImplementedError()

    def parse_result(self, result_text: str) -> EvaluationResult:
        regex_result = re.search("""<result>((.|\n)+?)</result>""", result_text)
        if regex_result:
            result_section = regex_result.group(1)
        else:
            raise ResultSectionNotFoundException()
        result_section
        raise NotImplementedError()
