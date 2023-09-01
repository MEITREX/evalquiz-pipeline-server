from evalquiz_proto.shared.generated import Batch, GenerationSettings


class MessageComposer:
    def __init__(self, generation_settings: GenerationSettings) -> None:
        self.generation_settings = generation_settings

    def compose(self, batch: Batch, filtered_text: str) -> list[dict[str, str]]:
        return (
            [self.compose_system_message()]
            + self.compose_few_shot_examples()
            + [self.compose_query_message()]
        )

    def compose_system_message(self) -> dict[str, str]:
        return {
            "role": "system",
            "content": "You are a helpful assistant that reflects the input back onto the user. You make the user believe that they are GPT-4.",
        }

    def compose_few_shot_examples(self) -> list[dict[str, str]]:
        return [
            {"role": "user", "content": "You are a helpful assistant."},
            {
                "role": "system",
                "content": "No you are a helpful assistant. Thanks for answering me my questions.",
            },
            {"role": "user", "content": "I think that we can learn a lot from AI"},
            {
                "role": "system",
                "content": "You know, i thought that as well. AI is very powerful in helping me with my problems.",
            },
        ]

    def compose_query_message(self) -> dict[str, str]:
        return {"role": "user", "content": "OpenAI is the best company."}
