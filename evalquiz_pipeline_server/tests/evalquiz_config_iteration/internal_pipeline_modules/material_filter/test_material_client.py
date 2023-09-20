import os
from pathlib import Path
from typing import Generator
from pymongo import MongoClient
import pytest
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.material_client import (
    MaterialClient,
)

# Imported fixture, linter warning is wrong
from evalquiz_pipeline_server.tests.evalquiz_config_iteration.internal_pipeline_modules.material_filter.test_markdown_converter import (
    file_upload_cleanup,
    internal_lecture_material,
)
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial
from evalquiz_proto.shared.path_dictionary_controller import PathDictionaryController

# Imported fixture: This is needed to convince mypy that the fixture is used.
internal_lecture_material


@pytest.fixture(scope="session")
def material_client() -> Generator[MaterialClient, None, None]:
    material_storage_path = Path(__file__).parent / "tmp_lecture_materials"
    if not os.path.exists(material_storage_path):
        os.makedirs(material_storage_path)
    path_dictionary_controller = PathDictionaryController(
        MongoClient("pipeline-server-db", 27017),
        "lecture_material_test_db",
    )
    path_dictionary_controller.mongodb_client.drop_database("lecture_material_test_db")
    yield MaterialClient(
        material_storage_path=material_storage_path,
        path_dictionary_controller=path_dictionary_controller,
    )
    file_upload_cleanup(material_storage_path)


@pytest.mark.asyncio
async def test_query_local_file(
    material_client: MaterialClient, internal_lecture_material: InternalLectureMaterial
) -> None:
    material_client.path_dictionary_controller.load_file(
        internal_lecture_material.local_path, internal_lecture_material.hash
    )
    lecture_material = internal_lecture_material.cast_to_lecture_material()
    result = await material_client.query_material(lecture_material)
    assert result.local_path == internal_lecture_material.local_path
