from abc import ABC, abstractmethod
from typing import Any
from evalquiz_proto.shared.generated import PipelineModule, QuestionType


class QuestionTypeComposer(PipelineModule, ABC):
    """Specific instructions to give according to a QuestionType."""

    def __init__(
        self,
        question_type: QuestionType,
    ):
        self.question_type = question_type

    @abstractmethod
    def compose_system_message_instructions(self) -> str:
        pass

    @abstractmethod
    def compose_few_shot_examples(self) -> list[dict[str, str]]:
        pass

    @abstractmethod
    def compose_query_message(self, filtered_text: str) -> dict[str, str]:
        pass
