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

# Imported fixture, linter warning is wrong
from evalquiz_pipeline_server.tests.evalquiz_config_iteration.internal_pipeline_modules.material_filter.test_material_client import (
    material_client,
)

# Imported fixture, linter warning is wrong
from evalquiz_pipeline_server.tests.evalquiz_config_iteration.internal_pipeline_modules.material_filter.test_markdown_converter import (
    markdown_converter,
)
from evalquiz_proto.shared.generated import (
    Batch,
    Capability,
    EducationalObjective,
    LectureMaterial,
    Relationship,
)
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial


def internal_lecture_material(
    local_path: Path, file_type: str
) -> InternalLectureMaterial:
    """Pytest fixture of InternalLectureMaterial.
    Creates InternalLectureMaterial from .lecture_materials/example_latex.tex.

    Returns:
        InternalLectureMaterial: _description_
    """
    material_metadata = LectureMaterial(
        reference="Example material", file_type=file_type
    )
    material_storage_path = local_path
    material = InternalLectureMaterial(material_storage_path, material_metadata)
    return material


example_latex_internal_lecture_material = internal_lecture_material(
    Path(__file__).parent / "lecture_materials/example_latex.tex", "application/x-tex"
)

selection_sort_wiki_internal_lecture_material = internal_lecture_material(
    Path(__file__).parent / "lecture_materials/selection_sort_wiki.html", "text/html"
)

testdoc_1_internal_lecture_material = internal_lecture_material(
    Path(__file__).parent / "lecture_materials/testdoc_1.md", "text/markdown"
)

pse_vu9_vererbung_internal_lecture_material = internal_lecture_material(
    Path(__file__).parent / "lecture_materials/pse_vu9_vererbung.pptx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
)


@pytest.fixture(scope="session")
def material_filter(
    material_client: MaterialClient, markdown_converter: MarkdownConverter
) -> MaterialFilter:
    material_client.path_dictionary_controller.load_file(
        example_latex_internal_lecture_material.local_path,
        example_latex_internal_lecture_material.hash,
    )
    material_client.path_dictionary_controller.load_file(
        selection_sort_wiki_internal_lecture_material.local_path,
        selection_sort_wiki_internal_lecture_material.hash,
    )
    material_client.path_dictionary_controller.load_file(
        testdoc_1_internal_lecture_material.local_path,
        testdoc_1_internal_lecture_material.hash,
    )
    material_client.path_dictionary_controller.load_file(
        pse_vu9_vererbung_internal_lecture_material.local_path,
        pse_vu9_vererbung_internal_lecture_material.hash,
    )
    material_filter = MaterialFilter(material_client, markdown_converter)
    return material_filter


inputs = [DefaultInternalConfig() for _ in range(4)]

inputs[0].batches.append(
    Batch(
        [example_latex_internal_lecture_material],
        [],
        [
            Capability(
                ["topicalization"],
                EducationalObjective.KNOW_AND_UNDERSTAND,
                Relationship.COMPLEX,
            )
        ],
    )
)

inputs[1].batches.append(
    Batch(
        [selection_sort_wiki_internal_lecture_material],
        [],
        [
            Capability(
                ["complexity"],
                EducationalObjective.KNOW_AND_UNDERSTAND,
                Relationship.COMPLEX,
            )
        ],
    )
)

inputs[2].batches.append(
    Batch(
        [testdoc_1_internal_lecture_material],
        [],
        [
            Capability(
                ["entrypoint"],
                EducationalObjective.KNOW_AND_UNDERSTAND,
                Relationship.DIFFERENCES,
            )
        ],
    )
)

inputs[3].batches.append(
    Batch(
        [pse_vu9_vererbung_internal_lecture_material],
        [],
        [
            Capability(
                ["extends", "abstract"],
                EducationalObjective.KNOW_AND_UNDERSTAND,
                Relationship.COMPLEX,
            )
        ],
    )
)


@pytest.mark.parametrize("input", inputs)
@pytest.mark.asyncio
async def test_run(
    material_filter: MaterialFilter,
    input: DefaultInternalConfig,
) -> None:
    (_, result) = await material_filter.run(input)
    assert input.batches[0].capabilites[0].keywords[0] in result[0]
