from pathlib import Path
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.question_type_composer import (
    QuestionTypeComposer,
)
from evalquiz_proto.shared.generated import MultipleResponse, QuestionType


class MultipleResponseComposer(QuestionTypeComposer):
    def __init__(self) -> None:
        question_type = QuestionType.MULTIPLE_RESPONSE
        super().__init__(
            question_type,
            MultipleResponse(
                "QUESTION_TEXT",
                ["ANSWER_TEXT_1", "ANSWER_TEXT_2"],
                ["DISTRACTOR_TEXT_1", "DISTRACTOR_TEXT_2"],
            ),
            Path(__file__).parent / "few_shot_examples",
        )

    def compose_query_message(self) -> str:
        raise NotImplementedError()
