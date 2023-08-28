from evalquiz_proto.shared.generated import GenerationSettings


class DefaultInternalConfig:
    def __init__(self) -> None:
        self.generation_settings = GenerationSettings(model="gpt-4")
