import re
import time
from typing import Any, Optional, cast
from evalquiz_pipeline_server.evalquiz_config_iteration.default_internal_config import (
    DefaultInternalConfig,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.message_composer import (
    MessageComposer,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.result_exceptions import (
    ResultException,
    ResultSectionNotFoundException,
    ResultSectionNotParsableException,
)
from evalquiz_pipeline_server.pipeline_execution.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import (
    Batch,
    CourseSettings,
    GenerationSettings,
    InternalConfig,
    MultipleChoice,
    MultipleResponse,
    PipelineModule,
    QuestionType,
    Result,
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
    def __init__(self, max_request: int = 4, api_request_timeout: int = 12) -> None:
        pipeline_module = PipelineModule(
            "question_generation",
            "tuple[InternalConfig, list[str]]",
            "InternalConfig",
        )
        super().__init__(pipeline_module)
        self.max_requests = max_request
        self.api_request_timeout = api_request_timeout
        self.default_internal_config = DefaultInternalConfig()

    async def run(self, input: Any) -> Any:
        (internal_config, filtered_texts) = cast(
            tuple[InternalConfig, list[str]], input
        )
        course_settings = self.resolve_course_settings(internal_config)
        generation_settings = self.resolve_generation_settings(internal_config)
        model = self.resolve_model(internal_config)
        message_composer = MessageComposer(course_settings, generation_settings)
        for batch, filtered_text in zip(internal_config.batches, filtered_texts):
            self.process_batch(batch, filtered_text, message_composer, model)
        return internal_config

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

    def resolve_model(self, internal_config: InternalConfig) -> str:
        if (
            internal_config.generation_settings is not None
            and internal_config.generation_settings.model is not None
        ):
            return internal_config.generation_settings.model
        elif (
            self.default_internal_config.generation_settings is not None
            and self.default_internal_config.generation_settings.model is not None
        ):
            return self.default_internal_config.generation_settings.model
        else:
            raise ValueError("DefaultInternalConfig not specified correctly.")

    def process_batch(
        self,
        batch: Batch,
        filtered_text: str,
        message_composer: MessageComposer,
        model: str,
    ) -> None:
        previous_messages: list[dict[str, str]] = []
        for question in batch.question_to_generate:
            messages = message_composer.compose(
                question,
                batch.capabilites,
                filtered_text,
                previous_messages,
            )
            result = self.request_result(question.question_type, messages, model)
            question.result = result

    def request_result(
        self, question_type: QuestionType, messages: list[dict[str, str]], model: str
    ) -> Optional[Result]:
        result = Result()
        for _ in range(self.max_requests):
            try:
                completion = openai.ChatCompletion.create(
                    deployment_id="EvalQuiz-GPT4", model=model, messages=messages
                )
                result_text = completion["choices"][0]["message"]["content"]
                result = self.parse_result(question_type, result_text)
                #time.sleep(self.api_request_timeout)
            except ResultException:
                pass
        return result

    def parse_result(self, question_type: QuestionType, result_text: str) -> Result:
        regex_result = re.search("""<result>((.|\n)+?)</result>""", result_text)
        if regex_result:
            result_section = regex_result.group(1)
        else:
            raise ResultSectionNotFoundException()
        match question_type:
            case QuestionType.MULTIPLE_CHOICE:
                multiple_choice = MultipleChoice().from_json(result_section)
                return Result(multiple_choice=multiple_choice)
            case QuestionType.MULTIPLE_RESPONSE:
                multiple_response = MultipleResponse().from_json(result_section)
                return Result(multiple_response=multiple_response)
            case _:
                raise ResultSectionNotParsableException()
