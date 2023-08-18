from pathlib import Path
import pytest
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.markdown_converter import (
    MarkdownConverter,
)
from evalquiz_proto.shared.generated import LectureMaterial
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial


@pytest.fixture(scope="session")
def internal_lecture_material() -> InternalLectureMaterial:
    material_metadata = LectureMaterial(
        reference="Example textfile", file_type="text/html"
    )
    path = Path(__file__).parent / "example_materials/example.html"
    material = InternalLectureMaterial(path, material_metadata)
    return material


def test_convert_material(internal_lecture_material: InternalLectureMaterial) -> None:
    assert internal_lecture_material.file_type == "text/html"
    markdown_converter = MarkdownConverter()
    internal_lecture_material_md = markdown_converter.convert_material(
        internal_lecture_material
    )
    assert internal_lecture_material_md.file_type == "text/markdown"
    path_stem = internal_lecture_material.local_path.stem
    assert markdown_converter.path_dictionary_controller.get_file_path_from_hash(
        internal_lecture_material_md.hash
    ) == markdown_converter.material_storage_path / (path_stem + ".md")
