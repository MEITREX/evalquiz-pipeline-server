import glob
import os
from pathlib import Path
from typing import Generator
import pytest
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.markdown_converter import (
    MarkdownConverter,
)
from evalquiz_proto.shared.generated import LectureMaterial
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial
from evalquiz_proto.shared.path_dictionary_controller import PathDictionaryController


@pytest.fixture(scope="session")
def internal_lecture_material() -> InternalLectureMaterial:
    """Pytest fixture of InternalLectureMaterial.
    Creates InternalLectureMaterial from .lecture_materials/example.html.

    Returns:
        InternalLectureMaterial: _description_
    """
    material_metadata = LectureMaterial(
        reference="Example textfile", file_type="text/html"
    )
    material_storage_path = Path(__file__).parent / "lecture_materials/example.html"
    material = InternalLectureMaterial(material_storage_path, material_metadata)
    return material


@pytest.fixture(scope="session")
def markdown_converter() -> Generator[MarkdownConverter, None, None]:
    """Pytest fixture of MarkdownConverter.
    Initializes MarkdownConverter with custom test database.
    Test database is emptied before tests are executed.
    Cleans up created files after test execution that uses this fixture.

    Yields:
        Generator[MarkdownConverter, None, None]: Generator with one MarkdownConverter element. Yielded until file cleanup.
    """
    material_storage_path = Path(__file__).parent / "lecture_materials_markdown"
    if not os.path.exists(material_storage_path):
        os.makedirs(material_storage_path)
    path_dictionary_controller = PathDictionaryController(
        mongodb_database="lecture_material_markdown_test_db"
    )
    path_dictionary_controller.mongodb_client.drop_database(
        "lecture_material_markdown_test_db"
    )
    yield MarkdownConverter(material_storage_path, path_dictionary_controller)
    file_upload_cleanup(material_storage_path)


def delete_all_files_in_folder(folder_path: Path) -> None:
    """Deletes all files in a folder, non-recursive.

    Args:
        folder_path (Path): Path to the folder.
    """
    files = glob.glob(str(folder_path / "*"))
    for local_file in files:
        os.remove(local_file)


def file_upload_cleanup(material_storage_path: Path) -> None:
    """Deletes files that were uploaded for test purposes.

    Args:
        material_storage_path (Path): The path were the uploaded files are stored.
    """
    delete_all_files_in_folder(material_storage_path)
    os.rmdir(material_storage_path)


def test_convert_material(
    internal_lecture_material: InternalLectureMaterial,
    markdown_converter: MarkdownConverter,
) -> None:
    assert internal_lecture_material.file_type == "text/html"
    internal_lecture_material_md = markdown_converter.convert_material(
        internal_lecture_material
    )
    assert internal_lecture_material_md.file_type == "text/markdown"
    path_stem = internal_lecture_material.local_path.stem
    assert markdown_converter.path_dictionary_controller.get_file_path_from_hash(
        internal_lecture_material_md.hash
    ) == markdown_converter.material_storage_path / (path_stem + ".md")