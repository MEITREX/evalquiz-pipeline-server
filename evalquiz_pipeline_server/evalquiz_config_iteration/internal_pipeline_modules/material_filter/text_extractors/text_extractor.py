from abc import ABC, abstractmethod
from evalquiz_proto.shared.generated import Capability


class TextExtractor(ABC):
    def __init__(self, max_tokens: int):
        self.max_tokens = max_tokens

    @abstractmethod
    def extract_with_capabilites(
        self, text: list[str], capabilites: list[Capability]
    ) -> str:
        pass
