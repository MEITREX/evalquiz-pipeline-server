import re
import betterproto
from evalquiz_pipeline_server.evalquiz_config_iteration.api_client_registry import (
    APIClientRegistry,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.evaluation_type_composer.categorical_composer import (
    CategoricalComposer,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.evaluation_type_composer.evaluation_result_type_composer import (
    EvaluationResultTypeComposer,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.evaluation_type_composer.value_range_composer import (
    ValueRangeComposer,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.internal_evaluations.internal_evaluation import (
    InternalEvaluation,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.generation_result_template import (
    GenerationResultTemplate,
)
from evalquiz_proto.shared.exceptions import (
    EvaluationNotCompatibleWithInternalEvaluation,
    ResultSectionNotFoundException,
    ResultSectionNotParsableException,
)
from evalquiz_proto.shared.generated import (
    Evaluation,
    EvaluationResult,
    EvaluationResultType,
    GenerationEvaluationResult,
    GenerationResult,
    LanguageModelEvaluation,
)


class InternalLanguageModelEvaluation(InternalEvaluation):
    def __init__(self) -> None:
        evaluation_type = "language_model_evaluation"
        super().__init__(evaluation_type)
        self.api_client_registry = APIClientRegistry()
        self.evaluation_type_composers: dict[str, EvaluationResultTypeComposer] = {
            "value_range": ValueRangeComposer(),
            "categorical": CategoricalComposer(),
        }
        self.generation_result_template = GenerationResultTemplate()

    def evaluate(
        self, evaluation: Evaluation, generation_result: GenerationResult
    ) -> EvaluationResult:
        (_, language_model_evaluation) = betterproto.which_one_of(
            evaluation, "evaluation"
        )
        if language_model_evaluation is None or not isinstance(
            language_model_evaluation, LanguageModelEvaluation
        ):
            raise EvaluationNotCompatibleWithInternalEvaluation()
        llm_client = self.api_client_registry.llm_clients[
            language_model_evaluation.model
        ]
        messages = self.compose_messages(language_model_evaluation, generation_result)
        result_text = llm_client.request_result_text(messages)
        return self.parse_result(
            result_text, language_model_evaluation.evaluation_result_type
        )

    def compose_messages(
        self,
        language_model_evaluation: LanguageModelEvaluation,
        generation_result: GenerationResult,
    ) -> list[dict[str, str]]:
        return (
            [self.compose_system_message()]
            + self.compose_few_shot_examples(
                language_model_evaluation.evaluation_result_type,
                language_model_evaluation.evaluation_description,
                language_model_evaluation.few_shot_examples,
            )
            + [
                self.compose_query_message(
                    language_model_evaluation.evaluation_result_type,
                    language_model_evaluation.evaluation_description,
                    generation_result,
                )
            ]
        )

    def compose_system_message(self) -> dict[str, str]:
        return {
            "role": "system",
            "content": """You are a question evaluation assistant that supports evaluating questions in multiple fixed formats.

The evaluation generated by you serves the purpose of helping a teacher to gather more insight over a specific question.
""",
        }

    def compose_few_shot_examples(
        self,
        evaluation_result_type: EvaluationResultType,
        evaluation_description: str,
        generation_evaluation_results: list[GenerationEvaluationResult],
    ) -> list[dict[str, str]]:
        few_shot_example_messages: list[dict[str, str]] = []
        (type, _) = betterproto.which_one_of(
            evaluation_result_type, "evaluation_result_type"
        )
        for generation_evaluation_result in generation_evaluation_results:
            user_example_message = self.compose_query_message(
                evaluation_result_type,
                evaluation_description,
                generation_evaluation_result.generation_result,
            )
            evaluation_type_composer = self.evaluation_type_composers[type]
            assistant_example = evaluation_type_composer.result_template(
                generation_evaluation_result.evaluation_result
            )
            few_shot_example_messages.append(user_example_message)
            few_shot_example_messages.append(
                {"role": "assistant", "content": assistant_example}
            )
        return few_shot_example_messages

    def compose_query_message(
        self,
        evaluation_result_type: EvaluationResultType,
        evaluation_description: str,
        generation_result: GenerationResult,
    ) -> dict[str, str]:
        (type, _) = betterproto.which_one_of(
            evaluation_result_type, "evaluation_result_type"
        )
        evaluation_type_composer = self.evaluation_type_composers[type]
        evaluation_type_query_message = evaluation_type_composer.compose_query_message(
            evaluation_result_type
        )
        content = (
            """Your goal is to evaluate the question in the following JSON format:

"""
            + evaluation_type_query_message
            + """Description how the question should be evaluated:

"""
            + evaluation_description
            + """
Question to evaluate:

"""
            + self.generation_result_template.result_template(generation_result)
        )
        return {"role": "user", "content": content}

    def parse_result(
        self, result_text: str, evaluation_result_type: EvaluationResultType
    ) -> EvaluationResult:
        regex_result = re.search(
            """<result type=evaluation>((.|\n)+?)</result>""", result_text
        )
        if regex_result:
            result_section = regex_result.group(1)
        else:
            raise ResultSectionNotFoundException()
        (type, _) = betterproto.which_one_of(
            evaluation_result_type, "evaluation_result_type"
        )
        match type:
            case "value_range":
                try:
                    float_value = float(result_section)
                except Exception:
                    raise ResultSectionNotParsableException()
                return EvaluationResult(float_value=float_value)
            case "categorical":
                return EvaluationResult(str_value=result_section)
            case _:
                raise ResultSectionNotParsableException()
