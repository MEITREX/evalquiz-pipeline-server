from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def request_result_text(self, messages: list[dict[str, str]]) -> str:
        pass
