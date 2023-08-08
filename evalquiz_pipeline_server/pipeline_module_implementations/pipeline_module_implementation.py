from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from evalquiz_proto.shared.generated import PipelineModule

class PipelineModuleImplementation(PipelineModule):

    def __init__(self, description: str):
        self.description = description

    @abstractmethod
    def run(input: Any) -> Any:
        pass
