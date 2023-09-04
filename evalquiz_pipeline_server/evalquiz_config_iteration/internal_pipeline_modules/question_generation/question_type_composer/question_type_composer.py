from abc import ABC, abstractmethod
from pathlib import Path
import betterproto
from evalquiz_proto.shared.generated import PipelineModule, QuestionType


class QuestionTypeComposer(PipelineModule, ABC):
    """Specific instructions to give according to a QuestionType."""

    def __init__(
        self,
        question_type: QuestionType,
        question: betterproto.Message,
        few_shot_example_path: Path,
    ):
        self.question_type = question_type
        self.question = question
        self.few_shot_example_path = few_shot_example_path

    @abstractmethod
    def compose_query_message(self) -> str:
        pass

    def result_template(self) -> str:
        json_question = self.question.to_json(indent=4)
        return "\n<result>\n" + json_question + "\n</result>\n\n"
