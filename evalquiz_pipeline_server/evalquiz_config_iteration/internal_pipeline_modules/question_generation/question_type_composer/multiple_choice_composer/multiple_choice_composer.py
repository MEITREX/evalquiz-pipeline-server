from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.multiple_choice_composer.multiple_choice_few_shot_examples import (
    multiple_choice_few_shot_examples,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.question_type_composer import (
    QuestionTypeComposer,
)
from evalquiz_proto.shared.generated import MultipleChoice, QuestionType, Result


class MultipleChoiceComposer(QuestionTypeComposer):
    def __init__(self) -> None:
        question_type = QuestionType.MULTIPLE_CHOICE
        super().__init__(
            question_type,
            Result(
                multiple_choice=MultipleChoice(
                    "QUESTION_TEXT",
                    "ANSWER_TEXT",
                    ["DISTRACTOR_TEXT_1", "DISTRACTOR_TEXT_2"],
                )
            ),
            multiple_choice_few_shot_examples,
        )

    def compose_query_message(self) -> str:
        return (
            self.result_template()
            + """Where QUESTION_TEXT is the question.
ANSWER_TEXT the only valid answer to the question. And DISTRACTOR_TEXT_1, DISTRACTOR_TEXT_2 answer options that are false.

"""
        )
