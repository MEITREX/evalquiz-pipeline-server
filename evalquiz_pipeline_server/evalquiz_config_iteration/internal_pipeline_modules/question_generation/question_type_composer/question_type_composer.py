from abc import ABC, abstractmethod
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.few_shot_example import (
    FewShotExample,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.generation_result_template import (
    GenerationResultTemplate,
)
from evalquiz_proto.shared.generated import GenerationResult, QuestionType


class QuestionTypeComposer(ABC, GenerationResultTemplate):
    """Specific instructions to give according to a QuestionType."""

    def __init__(
        self,
        question_type: QuestionType,
        generation_result: GenerationResult,
        few_shot_examples: list[FewShotExample],
    ):
        self.question_type = question_type
        self.generation_result = generation_result
        self.few_shot_examples = few_shot_examples

    @abstractmethod
    def compose_query_message(self) -> str:
        pass
