from abc import ABC, abstractmethod
from evalquiz_proto.shared.generated import (
    Evaluation,
    EvaluationResult,
    GenerationResult,
)


class InternalEvaluation(ABC):
    def __init__(self, evaluation_type: str) -> None:
        self.evaluation_type = evaluation_type

    @abstractmethod
    def evaluate(
        self, evaluation: Evaluation, generation_result: GenerationResult
    ) -> EvaluationResult:
        pass
