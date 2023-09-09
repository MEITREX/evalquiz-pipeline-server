from evalquiz_proto.shared.generated import Capability, Question, GenerationResult


class FewShotExample:
    def __init__(
        self,
        question: Question,
        capabilites: list[Capability],
        filtered_text: str,
        generation_result: GenerationResult,
    ):
        self.question = question
        self.capabilites = capabilites
        self.filtered_text = filtered_text
        self.generation_result = generation_result
