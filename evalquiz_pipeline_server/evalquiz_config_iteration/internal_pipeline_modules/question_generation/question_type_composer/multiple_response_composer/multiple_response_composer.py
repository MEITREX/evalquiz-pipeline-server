from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.multiple_response_composer.multiple_response_few_shot_examples import (
    multiple_response_few_shot_examples,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.question_type_composer import (
    QuestionTypeComposer,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.generation_result_template import (
    GenerationResultTemplate,
)
from evalquiz_proto.shared.generated import (
    MultipleResponse,
    QuestionType,
    GenerationResult,
)


class MultipleResponseComposer(QuestionTypeComposer, GenerationResultTemplate):
    def __init__(self) -> None:
        question_type = QuestionType.MULTIPLE_RESPONSE
        super().__init__(
            question_type,
            GenerationResult(
                multiple_response=MultipleResponse(
                    "QUESTION_TEXT",
                    ["ANSWER_TEXT_1", "ANSWER_TEXT_2"],
                    ["DISTRACTOR_TEXT_1", "DISTRACTOR_TEXT_2"],
                )
            ),
            multiple_response_few_shot_examples,
        )

    def compose_query_message(self) -> str:
        return (
            self.result_template(self.generation_result)
            + """Where QUESTION_TEXT is the question.
ANSWER_TEXT_1 and ANSWER_TEXT_2 are the only valid answers to the question. And DISTRACTOR_TEXT_1, DISTRACTOR_TEXT_2 answer options that are false.

The total amount af answer texts + distractor texts is always 4. But different combinations of answer texts and distractor texts are allowed.

- DISTRACTOR_TEXT_1, DISTRACTOR_TEXT_2, DISTRACTOR_TEXT_3, DISTRACTOR_TEXT_4
- ANSWER_TEXT_1, DISTRACTOR_TEXT_1, DISTRACTOR_TEXT_2, DISTRACTOR_TEXT_3
- ANSWER_TEXT_1, ANSWER_TEXT_2, ANSWER_TEXT_3, DISTRACTOR_TEXT_1
- ANSWER_TEXT_1, ANSWER_TEXT_2, ANSWER_TEXT_3, ANSWER_TEXT_4

"""
        )
