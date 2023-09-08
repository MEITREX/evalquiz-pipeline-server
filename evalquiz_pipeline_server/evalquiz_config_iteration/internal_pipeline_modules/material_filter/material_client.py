import mimetypes
from pathlib import Path
from typing import AsyncIterator
import betterproto
from grpclib.client import Channel
from evalquiz_proto.shared.exceptions import (
    FirstDataChunkNotMetadataException,
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
from evalquiz_proto.shared.path_dictionary_controller import (
    PathDictionaryController,
)


class MaterialClient:
    def __init__(
        self,
        material_server_urls: list[str] = [],
        material_storage_path: Path = Path(__file__).parent / "lecture_materials",
        path_dictionary_controller: PathDictionaryController = PathDictionaryController(),
    ) -> None:
        """Constructor of MaterialClient.

        Args:
            material_server_urls (list[str]): A list of URLs where material servers can be found. Defaults to [].
            material_storage_path (Path, optional): Specifies the path where lecture materials are stored. Defaults to Path(__file__).parent/"lecture_materials".
            path_dictionary_controller (PathDictionaryController): Component for managing lecture material file accesses on system.
        """
        self.material_server_port = 28390
        self.request_timeout_seconds = 2.0
        self.material_server_urls = material_server_urls
        self.material_storage_path = material_storage_path
        self.path_dictionary_controller = path_dictionary_controller

    async def query_material(
        self, lecture_material: LectureMaterial
    ) -> InternalLectureMaterial:
        """Queries lecture material from PathDictionaryController.
        If lecture material is not available in PathDictionaryController it is queried remotely and added to PathDictionaryController,
        then returned as InternalLectureMaterial.

        Args:
            lecture_material (LectureMaterial): LectureMaterial containing hash for the query.

        Returns:
            InternalLectureMaterial:
        """
        try:
            local_path = self.path_dictionary_controller.get_file_path_from_hash(
                lecture_material.hash
            )
            return InternalLectureMaterial(local_path, lecture_material)
        except KeyError:
            await self.add_to_path_dictionary_controller_from_server(lecture_material)
            local_path = self.path_dictionary_controller.get_file_path_from_hash(
                lecture_material.hash
            )
            return InternalLectureMaterial(local_path, lecture_material)

    async def add_to_path_dictionary_controller_from_server(
        self, request_lecture_material: LectureMaterial
    ) -> None:
        """Queries remotes for lecture material data and adds it to PathDictionaryController.

        Args:
            request_lecture_material (LectureMaterial): LectureMaterial containing hash for the remote query.

        Raises:
            NoMimetypeMappingException
            FirstDataChunkNotMetadataException
        """
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
            local_path = local_path.parent / (local_path.stem + extension)
            async_iterator_bytes = self._to_async_iterator_bytes(
                material_upload_data_iterator
            )
            await self.path_dictionary_controller.add_file_async(
                local_path,
                lecture_material.hash,
                async_iterator_bytes,
            )
        else:
            raise FirstDataChunkNotMetadataException()

    async def _to_async_iterator_bytes(
        self, material_upload_data_iterator: AsyncIterator[MaterialUploadData]
    ) -> AsyncIterator[bytes]:
        """Converts AsyncIterator[MaterialUploadData] to AsyncIterator[bytes] by runtime type checking/assertions.

        Args:
            material_upload_data_iterator (AsyncIterator[MaterialUploadData]): Iterator of MaterialUploadData.

        Returns:
            AsyncIterator[bytes]: Iterator of bytes.
        """
        material_upload_data = await material_upload_data_iterator.__anext__()
        (type, data) = betterproto.which_one_of(
            material_upload_data, "material_upload_data"
        )
        if data is not None and type == "data":
            yield data
        else:
            TypeError(
                "AsyncIterator[MaterialUploadData] cannot be converted into AsyncIterator[bytes]."
            )

    async def get_material_upload_data_iterator(
        self, lecture_material: LectureMaterial
    ) -> AsyncIterator[MaterialUploadData]:
        """Builds priority list of URLs and tries to connect to a server in the list.
        Then tries to get an asynchronous lecture material iterator and returns it, if successful.

        Args:
            lecture_material (LectureMaterial): LectureMaterial containing hash for the remote query.

        Raises:
            LectureMaterialNotFoundOnRemotesException

        Returns:
            AsyncIterator[MaterialUploadData]: An iterator with its first element as Metadata followed by binary packets.
        """
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
