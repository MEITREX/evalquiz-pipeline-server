from typing import Any, List, Optional
from evalquiz_pipeline_server.evalquiz_config_iteration.default_internal_config import (
    DefaultInternalConfig,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.markdown_converter import (
    MarkdownConverter,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.material_client import (
    MaterialClient,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.text_extractors.text_extractor import (
    TextExtractor,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.text_extractors.topic_extension_text_extractor import (
    TopicExtensionTextExtractor,
)
from evalquiz_pipeline_server.pipeline_execution.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import Batch, InternalConfig, PipelineModule
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial
import tiktoken


class MaterialFilter(InternalPipelineModule):
    def __init__(
        self,
        material_client: Optional[MaterialClient] = None,
        markdown_converter: MarkdownConverter = MarkdownConverter(),
    ) -> None:
        pipeline_module = PipelineModule(
            "material_filter", "InternalConfig", "tuple[InternalConfig, list[str]]"
        )
        super().__init__(pipeline_module)
        self.material_client = material_client
        self.markdown_converter = markdown_converter
        self.default_internal_config = DefaultInternalConfig()

    async def run(self, input: Any) -> Any:
        if not isinstance(input, InternalConfig):
            raise TypeError()
        model = self.resolve_model(input)
        encode_function = tiktoken.encoding_for_model(model)
        material_client = self.material_client or MaterialClient(
            input.material_server_urls
        )
        text_extractor: TextExtractor = TopicExtensionTextExtractor(
            1000, encode_function.encode
        )
        return (
            input,
            [
                await self.process_batch(batch, material_client, text_extractor)
                for batch in input.batches
            ],
        )

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

    async def process_batch(
        self,
        batch: Batch,
        material_client: MaterialClient,
        text_extractor: TextExtractor,
    ) -> str:
        internal_lecture_materials_md = (
            await self.collect_internal_lecture_materials_md_for_batch(
                batch, material_client
            )
        )
        internal_lecture_material_contents = (
            self.collect_internal_lecture_material_contents(
                internal_lecture_materials_md
            )
        )
        extracted_text = text_extractor.extract_with_capabilites(
            internal_lecture_material_contents, batch.capabilites
        )
        return extracted_text

    async def collect_internal_lecture_materials_md_for_batch(
        self,
        batch: Batch,
        material_client: MaterialClient,
    ) -> List[InternalLectureMaterial]:
        internal_lecture_materials_md: List[InternalLectureMaterial] = []
        for lecture_material in batch.lecture_materials:
            internal_lecture_material = await material_client.query_material(
                lecture_material
            )
            internal_lecture_material_md = self.markdown_converter.convert_material(
                internal_lecture_material
            )
            internal_lecture_materials_md.append(internal_lecture_material_md)
        return internal_lecture_materials_md

    def collect_internal_lecture_material_contents(
        self, internal_lecture_materials: List[InternalLectureMaterial]
    ) -> List[str]:
        contents: List[str] = []
        for internal_lecture_material in internal_lecture_materials:
            local_path = internal_lecture_material.local_path
            with open(local_path, "r") as local_file:
                content = local_file.read()
                contents.append(content)
        return contents
