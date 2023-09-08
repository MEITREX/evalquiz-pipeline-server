from abc import ABC, abstractmethod
from evalquiz_proto.shared.generated import EvaluationType


class EvaluationImplementation(ABC):
    def __init__(self, evaluation_type: EvaluationType) -> None:
        self.evaluation_type = evaluation_type

    @abstractmethod
    def evaluate(self) -> str:
        pass
