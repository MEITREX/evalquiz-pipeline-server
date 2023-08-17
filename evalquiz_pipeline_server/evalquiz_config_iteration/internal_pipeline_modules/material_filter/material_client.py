import mimetypes
from pathlib import Path
from typing import AsyncIterator
import betterproto
from grpclib.client import Channel
from evalquiz_proto.shared.exceptions import (
    FirstDataChunkNotLectureMaterialException,
    LectureMaterialLocallyNotFoundException,
    LectureMaterialNotFoundOnRemotesException,
    NoMimetypeMappingException,
)
from evalquiz_proto.shared.generated import (
    LectureMaterial,
    MaterialServerStub,
    MaterialUploadData,
    String,
)
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial
from evalquiz_proto.shared.internal_material_controller import (
    InternalMaterialController,
)


class MaterialClient:
    def __init__(
        self,
        material_server_urls: list[str],
        material_storage_path: Path = Path(__file__).parent / "lecture_materials",
    ) -> None:
        self.material_server_port = 28390
        self.request_timeout_seconds = 2.0
        self.material_server_urls = material_server_urls
        self.material_storage_path = material_storage_path
        self.internal_material_controller = InternalMaterialController()

    async def resolve_material(
        self, lecture_material: LectureMaterial
    ) -> InternalLectureMaterial:
        try:
            local_path = self.internal_material_controller.get_material_path_from_hash(
                lecture_material.hash
            )
            return InternalLectureMaterial(local_path, lecture_material)
        except LectureMaterialLocallyNotFoundException:
            await self.add_to_internal_material_controller_from_server(lecture_material)
            local_path = self.internal_material_controller.get_material_path_from_hash(
                lecture_material.hash
            )
            return InternalLectureMaterial(local_path, lecture_material)

    async def add_to_internal_material_controller_from_server(
        self, request_lecture_material: LectureMaterial
    ) -> None:
        material_upload_data_iterator = await self.get_material_upload_data_iterator(
            request_lecture_material
        )
        material_upload_data = await material_upload_data_iterator.__anext__()
        (type, lecture_material) = betterproto.which_one_of(
            material_upload_data, "material_upload_data"
        )
        if lecture_material is not None and type == "lecture_material":
            extension = mimetypes.guess_extension(lecture_material.file_type)
            if extension is None:
                raise NoMimetypeMappingException()
            local_path = self.material_storage_path / lecture_material.hash
            local_path = local_path.parent / (local_path.name + extension)
            await self.internal_material_controller.add_material_async(
                local_path,
                lecture_material,
                material_upload_data_iterator,
            )
        raise FirstDataChunkNotLectureMaterialException()

    async def get_material_upload_data_iterator(
        self, lecture_material: LectureMaterial
    ) -> AsyncIterator[MaterialUploadData]:
        material_server_urls = [lecture_material.url, *self.material_server_urls]
        for url in material_server_urls:
            channel = Channel(host=url, port=self.material_server_port)
            service = MaterialServerStub(channel)
            try:
                material_upload_data_iterator = service.get_material(
                    String(lecture_material.hash), timeout=self.request_timeout_seconds
                )
                return material_upload_data_iterator
            except Exception:
                pass
        raise LectureMaterialNotFoundOnRemotesException()
