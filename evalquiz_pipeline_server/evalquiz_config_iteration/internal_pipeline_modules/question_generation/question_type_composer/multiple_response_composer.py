from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.question_type_composer import (
    QuestionTypeComposer,
)
from evalquiz_proto.shared.generated import QuestionType


class MultipleResponseComposer(QuestionTypeComposer):
    def __init__(self) -> None:
        question_type = QuestionType.MULTIPLE_RESPONSE
        super().__init__(question_type)

    def compose_system_message_instructions(self) -> str:
        raise NotImplementedError()

    def compose_few_shot_examples(self) -> list[dict[str, str]]:
        raise NotImplementedError()

    def compose_query_message(self) -> dict[str, str]:
        raise NotImplementedError()
