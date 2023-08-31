from pathlib import Path
from evalquiz_proto.shared.generated import LectureMaterial
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial
from evalquiz_proto.shared.path_dictionary_controller import PathDictionaryController
import subprocess


class MarkdownConverter:
    def __init__(
        self,
        material_storage_path: Path = (
            Path(__file__).parent / "lecture_materials_markdown"
        ),
        path_dictionary_controller: PathDictionaryController = PathDictionaryController(
            mongodb_database="lecture_materials_markdown_db"
        ),
    ) -> None:
        """Constructor of MarkdownConverter.

        Args:
            material_storage_path (Path, optional): Path to where the generated markdown files should be stored. Defaults to ( Path(__file__).parent / "lecture_materials_markdown" ).
            path_dictionary_controller (PathDictionaryController, optional): PathDictionaryController manages references from unconverted lecture materials to their converted markdown versions. Defaults to PathDictionaryController( mongodb_database="lecture_materials_markdown_db" ).
        """
        self.path_dictionary_controller = path_dictionary_controller
        self.material_storage_path = material_storage_path

    def convert_material(
        self, internal_lecture_material: InternalLectureMaterial
    ) -> InternalLectureMaterial:
        """Converts InternalLectureMaterial to its markdown version.
        Retrieves converted version from self.path_dictionary_controller,
        otherwise a markdown version is generated and  added to self.path_dictionary_controller.

        Args:
            internal_lecture_material (InternalLectureMaterial): Input InternalLectureMaterial.

        Returns:
            InternalLectureMaterial: Converted output InternalLectureMaterial, which references a markdown document.
        """
        try:
            lecture_material = internal_lecture_material.cast_to_lecture_material()
            return self.retrieve_converted_material(lecture_material)
        except KeyError:
            internal_lecture_material_md = self.run_pandoc_conversion(
                internal_lecture_material
            )
            self.path_dictionary_controller.load_file(
                internal_lecture_material_md.local_path,
                internal_lecture_material_md.hash,
            )
            return internal_lecture_material_md

    def retrieve_converted_material(
        self, lecture_material: LectureMaterial
    ) -> InternalLectureMaterial:
        """Retrieves markdown converted InternalLectureMaterial from self.path_dictionary_controller.

        Args:
            lecture_material (LectureMaterial): LectureMaterial to retrieve.

        Returns:
            InternalLectureMaterial: Converted output InternalLectureMaterial, which references a markdown document.
        """
        local_path = self.path_dictionary_controller.get_file_path_from_hash(
            lecture_material.hash
        )
        return InternalLectureMaterial(local_path, lecture_material)

    def run_pandoc_conversion(
        self, internal_lecture_material: InternalLectureMaterial
    ) -> InternalLectureMaterial:
        """Runs subprocess with pandoc to convert file to markdown.

        Args:
            internal_lecture_material (InternalLectureMaterial): Input InternalLectureMaterial to convert.

        Returns:
            InternalLectureMaterial: Converted output InternalLectureMaterial, which references a markdown document.
        """
        input_path = internal_lecture_material.local_path
        output_path = self.material_storage_path / (input_path.stem + ".md")
        subprocess.run(["pandoc", input_path, "-o", output_path])
        output_lecture_material = internal_lecture_material.cast_to_lecture_material()
        output_lecture_material.file_type = "text/markdown"
        return InternalLectureMaterial(output_path, output_lecture_material)