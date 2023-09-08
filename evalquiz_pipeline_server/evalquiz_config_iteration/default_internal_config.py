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
        self.material_server_urls = []
        self.batches: list[Batch] = []
        self.course_settings = CourseSettings([], [], [])
        self.generation_settings = GenerationSettings(
            Mode(complete=Complete()), "gpt-4"
        )
        self.evaluation_settings: Optional[EvaluationSettings] = EvaluationSettings([])
