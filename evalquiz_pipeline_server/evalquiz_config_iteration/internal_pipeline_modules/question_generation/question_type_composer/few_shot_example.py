from evalquiz_proto.shared.generated import Capability, Question, Result


class FewShotExample:
    def __init__(
        self,
        question: Question,
        capabilites: list[Capability],
        filtered_text: str,
        result: Result,
    ):
        self.question = question
        self.capabilites = capabilites
        self.filtered_text = filtered_text
        self.result = result
