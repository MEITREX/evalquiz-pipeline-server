import betterproto
import pytest

from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.internal_evaluations.internal_language_model_evaluation import (
    InternalLanguageModelEvaluation,
)
from evalquiz_proto.shared.generated import (
    Categorical,
    Evaluation,
    EvaluationResult,
    EvaluationResultType,
    GenerationEvaluationResult,
    GenerationResult,
    LanguageModelEvaluation,
    MultipleChoice,
)


@pytest.fixture(scope="session")
def ilm_evaluation() -> InternalLanguageModelEvaluation:
    return InternalLanguageModelEvaluation()


@pytest.fixture(scope="session")
def language_model_evaluation() -> LanguageModelEvaluation:
    return LanguageModelEvaluation(
        "gpt-4",
        """Avoids terms that are associated with strong opinions or emotions.
Strongly value-laden terms (peace, war, crime, justice) should be avoided.
They provoke more extreme response behavior.
""",
        [
            GenerationEvaluationResult(
                GenerationResult(
                    multiple_choice=MultipleChoice(
                        "The hamster from the PSE hamster simulator is at war. How does they solve the labyrinth with the least amount of steps.",
                        "Picture A",
                        [
                            "Picture B",
                            "Picture C",
                        ],
                    )
                ),
                EvaluationResult(str_value="False"),
            )
        ],
        EvaluationResultType(categorical=Categorical(["True", "False"])),
    )


@pytest.fixture(scope="session")
def generation_result() -> GenerationResult:
    return GenerationResult(
        multiple_choice=MultipleChoice(
            "Which of the following terms is a ISO-OSI layers?",
            "Link",
            [
                "Rope",
                "Thread",
            ],
        )
    )


def test_compose_messages(
    ilm_evaluation: InternalLanguageModelEvaluation,
    language_model_evaluation: LanguageModelEvaluation,
    generation_result: GenerationResult,
) -> None:
    messages = ilm_evaluation.compose_messages(
        language_model_evaluation, generation_result
    )
    assert "Rope" in messages[3]["content"]


@pytest.mark.skip(reason="API call is made in every test run.")
def test_evaluate(
    ilm_evaluation: InternalLanguageModelEvaluation,
    language_model_evaluation: LanguageModelEvaluation,
    generation_result: GenerationResult,
) -> None:
    evaluation_result = ilm_evaluation.evaluate(
        Evaluation(language_model_evaluation=language_model_evaluation),
        generation_result,
    )
    (type, str_value) = betterproto.which_one_of(evaluation_result, "evaluation_result")
    assert type == "str_value"
    assert str_value == "True"
