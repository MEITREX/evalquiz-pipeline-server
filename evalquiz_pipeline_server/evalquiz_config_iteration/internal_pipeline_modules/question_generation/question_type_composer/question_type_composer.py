from abc import ABC, abstractmethod
from typing import Optional

import betterproto
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.few_shot_example import (
    FewShotExample,
)
from evalquiz_proto.shared.generated import GenerationResult, QuestionType


class QuestionTypeComposer(ABC):
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

    def result_template(self, generation_result: Optional[GenerationResult] = None) -> str:
        generation_result = generation_result or self.generation_result
        (_, result_value) = betterproto.which_one_of(generation_result, "generation_result")
        if result_value is None:
            raise ValueError(
                "GenerationResult is not set. GenerationResult template cannot be built."
            )
        json_result = result_value.to_json(indent=4)
        return "<result>\n" + json_result + "\n</result>\n\n"
