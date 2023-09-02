from typing import Any, cast
from evalquiz_pipeline_server.evalquiz_config_iteration.default_internal_config import (
    DefaultInternalConfig,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.message_composer import (
    MessageComposer,
)
from evalquiz_pipeline_server.pipeline_execution.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import (
    Batch,
    CourseSettings,
    GenerationSettings,
    InternalConfig,
    PipelineModule,
)
import openai

openai.api_type = "azure"
openai.api_version = "2023-08-01-preview"
with open("/run/secrets/openai_api_key") as openai_api_key:
    openai.api_key = openai_api_key.read().replace("\n", "")
openai.api_base = "https://evalquizuk.openai.azure.com/"
if openai.api_key is None:
    raise ValueError("OpenAI key is not set, therefore no requests can be made.")


class QuestionGeneration(InternalPipelineModule):
    def __init__(self) -> None:
        pipeline_module = PipelineModule(
            "question_generation",
            "tuple[InternalConfig, list[str]]",
            "tuple[InternalConfig, list[str]]",
        )
        super().__init__(pipeline_module)
        self.default_internal_config = DefaultInternalConfig()

    async def run(self, input: Any) -> Any:
        (internal_config, filtered_texts) = cast(
            tuple[InternalConfig, list[str]], input
        )
        course_settings = self.resolve_course_settings(internal_config)
        generation_settings = self.resolve_generation_settings(internal_config)
        message_composer = MessageComposer(course_settings, generation_settings)
        return (
            internal_config,
            [
                self.process_batch(batch, filtered_text, message_composer)
                for batch, filtered_text in zip(internal_config.batches, filtered_texts)
            ],
        )

    def resolve_generation_settings(
        self, internal_config: InternalConfig
    ) -> GenerationSettings:
        if internal_config.generation_settings is not None:
            return internal_config.generation_settings
        elif self.default_internal_config.generation_settings is not None:
            return self.default_internal_config.generation_settings
        else:
            raise ValueError("DefaultInternalConfig not specified correctly.")

    def resolve_course_settings(
        self, internal_config: InternalConfig
    ) -> CourseSettings:
        if internal_config.course_settings is not None:
            return internal_config.course_settings
        elif self.default_internal_config.course_settings is not None:
            return self.default_internal_config.course_settings
        else:
            raise ValueError("DefaultInternalConfig not specified correctly.")

    def process_batch(
        self,
        batch: Batch,
        filtered_text: str,
        message_composer: MessageComposer,
    ) -> list[str]:
        message_contents: list[str] = []
        previous_messages: list[dict[str, str]] = []
        for question in batch.question_to_generate:
            messages = message_composer.compose(
                question,
                batch.capabilites,
                filtered_text,
                previous_messages,
            )
            completion = openai.ChatCompletion.create(
                deployment_id="EvalQuiz-GPT4", model="gpt-4", messages=messages
            )
            result = completion["choices"][0]["message"]["content"]
            message_contents.append(result)
        return message_contents
