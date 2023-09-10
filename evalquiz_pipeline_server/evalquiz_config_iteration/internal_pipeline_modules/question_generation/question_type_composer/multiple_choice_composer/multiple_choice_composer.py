from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.multiple_choice_composer.multiple_choice_few_shot_examples import (
    multiple_choice_few_shot_examples,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.question_type_composer import (
    QuestionTypeComposer,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.generation_result_template import (
    GenerationResultTemplate,
)
from evalquiz_proto.shared.generated import (
    MultipleChoice,
    QuestionType,
    GenerationResult,
)


class MultipleChoiceComposer(QuestionTypeComposer, GenerationResultTemplate):
    def __init__(self) -> None:
        question_type = QuestionType.MULTIPLE_CHOICE
        QuestionTypeComposer.__init__(
            self,
            question_type,
            GenerationResult(
                multiple_choice=MultipleChoice(
                    "QUESTION_TEXT",
                    "ANSWER_TEXT",
                    ["DISTRACTOR_TEXT_1", "DISTRACTOR_TEXT_2"],
                )
            ),
            multiple_choice_few_shot_examples,
        )
        GenerationResultTemplate.__init__(self)

    def compose_query_message(self) -> str:
        return (
            self.result_template(self.generation_result)
            + """Where QUESTION_TEXT is the question.
ANSWER_TEXT the only valid answer to the question. And DISTRACTOR_TEXT_1, DISTRACTOR_TEXT_2 answer options that are false.

"""
        )
