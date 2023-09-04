from pathlib import Path
import pytest
from evalquiz_pipeline_server.evalquiz_config_iteration.default_internal_config import (
    DefaultInternalConfig,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.markdown_converter import (
    MarkdownConverter,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.material_client import (
    MaterialClient,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.material_filter import (
    MaterialFilter,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.pipelines.config_iteration_pipeline import (
    ConfigIterationPipeline,
)
from evalquiz_pipeline_server.pipeline_execution.pipeline_execution import (
    PipelineExecution,
)
from evalquiz_pipeline_server.tests.evalquiz_config_iteration.internal_pipeline_modules.material_filter.test_material_filter import (
    internal_lecture_material,
)
from evalquiz_proto.shared.generated import InternalConfig, PipelineStatus

# Imported fixture, linter warning is wrong
from evalquiz_pipeline_server.tests.evalquiz_config_iteration.internal_pipeline_modules.material_filter.test_material_client import (
    material_client,
)

# Imported fixture, linter warning is wrong
from evalquiz_pipeline_server.tests.evalquiz_config_iteration.internal_pipeline_modules.material_filter.test_markdown_converter import (
    markdown_converter,
)

# example_pptx_lecture_material = internal_lecture_material(
#    Path(__file__).parent / "~/Downloads",
#    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
# )


@pytest.fixture(scope="session")
def internal_config() -> InternalConfig:
    internal_config = DefaultInternalConfig()
    return internal_config


@pytest.fixture(scope="session")
def material_filter(
    material_client: MaterialClient, markdown_converter: MarkdownConverter
) -> MaterialFilter:
    # material_client.path_dictionary_controller.load_file(
    #    example_pptx_lecture_material.local_path, example_pptx_lecture_material.hash
    # )
    material_filter = MaterialFilter(material_client, markdown_converter)
    return material_filter


def test_composition() -> None:
    ConfigIterationPipeline()


@pytest.mark.asyncio
async def test_material_filter_and_question_generation_pipeline_execution(
    material_filter: MaterialFilter, internal_config: InternalConfig
) -> None:
    pipeline = ConfigIterationPipeline()
    pipeline.pipeline_modules = [material_filter, pipeline.pipeline_modules[1]]
    pipeline_execution = PipelineExecution(input, pipeline)
    # pipeline_status_iterator = pipeline_execution.run()
    # pipeline_statuses: list[PipelineStatus] = []
    # while True:
    #    try:
    #        pipeline_status = await pipeline_status_iterator.__anext__()
    #        pipeline_statuses.append(pipeline_status)
    #    except StopAsyncIteration:
    #        break
    # pass
