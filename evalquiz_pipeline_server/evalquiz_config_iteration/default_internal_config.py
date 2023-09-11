from typing import Optional
from evalquiz_proto.shared.generated import (
    Batch,
    Complete,
    CourseSettings,
    EvaluationSettings,
    GenerationSettings,
    InternalConfig,
    Mode,
)


class DefaultInternalConfig(InternalConfig):
    def __init__(self) -> None:
        material_server_urls: list[str] = []
        batches: list[Batch] = []
        course_settings = CourseSettings([], [], [])
        generation_settings = GenerationSettings(Mode(complete=Complete()), "gpt-4")
        evaluation_settings: Optional[EvaluationSettings] = EvaluationSettings([])
        super().__init__(
            material_server_urls,
            batches,
            course_settings,
            generation_settings,
            evaluation_settings,
        )
