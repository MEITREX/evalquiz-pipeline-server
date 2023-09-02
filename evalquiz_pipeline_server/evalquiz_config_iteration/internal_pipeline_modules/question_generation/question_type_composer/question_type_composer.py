from abc import ABC, abstractmethod
import betterproto
from evalquiz_proto.shared.generated import PipelineModule, Question, QuestionType


class QuestionTypeComposer(PipelineModule, ABC):
    """Specific instructions to give according to a QuestionType."""

    def __init__(self, question_type: QuestionType, question: betterproto.Message):
        self.question_type = question_type
        self.question = question

    @abstractmethod
    def compose_query_message(self) -> str:
        pass

    @abstractmethod
    def compose_few_shot_examples(self) -> list[dict[str, str]]:
        pass

    def result_template(self) -> str:
        json_question = self.question.to_json(indent=4)
        return "\n<result>\n" + json_question + "\n</result>\n\n"
