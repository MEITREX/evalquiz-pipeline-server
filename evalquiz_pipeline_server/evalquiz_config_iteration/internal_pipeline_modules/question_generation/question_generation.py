import re
from typing import Any, cast

from evalquiz_pipeline_server.evalquiz_config_iteration.api_client_registry import (
    APIClientRegistry,
)
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
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.shared_traits.question_reprocess_decider import (
    QuestionReprocessDecider,
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
    GenerationResult,
    Mode,
)


class QuestionGeneration(InternalPipelineModule, QuestionReprocessDecider):
    def __init__(self, max_request: int = 4, api_request_timeout: int = 12) -> None:
        pipeline_module = PipelineModule(
            "question_generation",
            "tuple[InternalConfig, list[str]]",
            "InternalConfig",
        )
        InternalPipelineModule.__init__(self, pipeline_module)
        QuestionReprocessDecider.__init__(self)
        self.default_internal_config = DefaultInternalConfig()
        self.api_client_registry = APIClientRegistry()
        self.max_requests = max_request
        self.api_request_timeout = api_request_timeout

    async def run(self, input: Any) -> Any:
        (internal_config, filtered_texts) = cast(
            tuple[InternalConfig, list[str]], input
        )
        course_settings = self.resolve_course_settings(internal_config)
        generation_settings = self.resolve_generation_settings(internal_config)
        model = self.resolve_model(internal_config)
        mode = self.resolve_mode(internal_config)
        message_composer = MessageComposer(course_settings, generation_settings)
        for batch, filtered_text in zip(internal_config.batches, filtered_texts):
            self.process_batch(batch, filtered_text, message_composer, model, mode)
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

    def resolve_mode(self, internal_config: InternalConfig) -> Mode:
        if (
            internal_config.generation_settings is not None
            and internal_config.generation_settings.mode is not None
        ):
            return internal_config.generation_settings.mode
        elif (
            self.default_internal_config.generation_settings is not None
            and self.default_internal_config.generation_settings.mode is not None
        ):
            return self.default_internal_config.generation_settings.mode
        else:
            raise ValueError("DefaultInternalConfig not specified correctly.")

    def process_batch(
        self,
        batch: Batch,
        filtered_text: str,
        message_composer: MessageComposer,
        model: str,
        mode: Mode,
    ) -> None:
        previous_messages: list[dict[str, str]] = []
        for question in batch.question_to_generate:
            if self.is_question_to_reprocess(question, mode):
                messages = message_composer.compose(
                    question,
                    batch.capabilites,
                    filtered_text,
                    previous_messages,
                )
                llm_client = self.api_client_registry.llm_clients[model]
                result_text = llm_client.request_result_text(
                    question.question_type, messages, model
                )
                try:
                    result = self.parse_result(question.question_type, result_text)
                except ResultException:
                    pass
                question.result = result
                question.evaluation = None

    def parse_result(
        self, question_type: QuestionType, result_text: str
    ) -> GenerationResult:
        regex_result = re.search("""<result>((.|\n)+?)</result>""", result_text)
        if regex_result:
            result_section = regex_result.group(1)
        else:
            raise ResultSectionNotFoundException()
        match question_type:
            case QuestionType.MULTIPLE_CHOICE:
                multiple_choice = MultipleChoice().from_json(result_section)
                return GenerationResult(multiple_choice=multiple_choice)
            case QuestionType.MULTIPLE_RESPONSE:
                multiple_response = MultipleResponse().from_json(result_section)
                return GenerationResult(multiple_response=multiple_response)
            case _:
                raise ResultSectionNotParsableException()
