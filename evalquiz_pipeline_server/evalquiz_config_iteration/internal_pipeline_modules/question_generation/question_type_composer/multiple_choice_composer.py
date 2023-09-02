from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.question_type_composer import (
    QuestionTypeComposer,
)
from evalquiz_proto.shared.generated import QuestionType


class MultipleChoiceComposer(QuestionTypeComposer):
    def __init__(self) -> None:
        question_type = QuestionType.MULTIPLE_CHOICE
        super().__init__(question_type)

    def compose_system_message_instructions(self) -> str:
        return ""

    def compose_few_shot_examples(self) -> list[dict[str, str]]:
        return []

    def compose_query_message(self, filtered_text: str) -> dict[str, str]:
        return {}
