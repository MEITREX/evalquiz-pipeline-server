from pathlib import Path
from typing import Any
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
from evalquiz_pipeline_server.tests.evalquiz_config_iteration.internal_pipeline_modules.material_filter.test_material_client import (
    material_client,
)
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


@pytest.fixture(scope="session")
def internal_lecture_material() -> InternalLectureMaterial:
    """Pytest fixture of InternalLectureMaterial.
    Creates InternalLectureMaterial from .lecture_materials/example_latex.tex.

    Returns:
        InternalLectureMaterial: _description_
    """
    material_metadata = LectureMaterial(
        reference="Example latex", file_type="application/x-tex"
    )
    material_storage_path = (
        Path(__file__).parent / "lecture_materials/example_latex.tex"
    )
    material = InternalLectureMaterial(material_storage_path, material_metadata)
    return material


@pytest.fixture(scope="session")
def material_filter(
    material_client: MaterialClient, markdown_converter: MarkdownConverter
) -> MaterialFilter:
    material_filter = MaterialFilter(material_client, markdown_converter)
    return material_filter


input_output_pairs = [
    (default_internal_config, (default_internal_config, ""))
    for default_internal_config in [DefaultInternalConfig() for _ in range(1)]
]

input_output_pairs[0][0].batches.append(
    Batch(
        [internal_lecture_material()],
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


@pytest.mark.parametrize("input, output", input_output_pairs)
def test_run(material_filter: MaterialFilter, input: Any, output: Any) -> None:
    result = material_filter.run(input)
