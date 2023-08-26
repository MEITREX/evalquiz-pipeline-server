from typing import Any, List
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.markdown_converter import (
    MarkdownConverter,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.material_client import (
    MaterialClient,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.text_extractors.topic_extension_text_extractor import (
    TopicExtensionTextExtractor,
)
from evalquiz_pipeline_server.pipeline_execution.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import Batch, InternalConfig, PipelineModule
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial


class MaterialFilter(InternalPipelineModule):
    def __init__(self) -> None:
        pipeline_module = PipelineModule(
            "material_filter", "InternalConfig", "Tuple[InternalConfig, str]"
        )
        super().__init__(pipeline_module)
        self.markdown_converter = MarkdownConverter()
        self.text_extractor = TopicExtensionTextExtractor(1000)

    async def run(self, input: Any) -> Any:
        if not isinstance(input, InternalConfig):
            raise TypeError()
        material_client = MaterialClient(input.material_server_urls)

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

    async def process_batch(
        self,
        batch: Batch,
        material_client: MaterialClient,
    ) -> List[str]:
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
        extracted_text = self.text_extractor.extract_with_capabilites(
            internal_lecture_material_contents, batch.capabilites
        )
