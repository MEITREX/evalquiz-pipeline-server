import pytest
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.message_composer import (
    MessageComposer,
)
from evalquiz_proto.shared.generated import (
    Capability,
    CourseSettings,
    EducationalObjective,
    GenerationSettings,
    Question,
    Relationship,
    QuestionType,
)


@pytest.fixture
def message_composer() -> MessageComposer:
    required_capabilites = [
        Capability(
            ["variable", "instantiation"],
            EducationalObjective.KNOW_AND_UNDERSTAND,
            Relationship.DIFFERENCES,
        )
    ]
    course_settings = CourseSettings([], required_capabilites, [])
    generation_settings = GenerationSettings()
    return MessageComposer(course_settings, generation_settings)


def test_compose_system_message(message_composer: MessageComposer) -> None:
    question = Question(QuestionType.MULTIPLE_CHOICE)
    capbilites = [
        Capability(
            ["stack", "heap"],
            EducationalObjective.KNOW_AND_UNDERSTAND,
            Relationship.COMPLEX,
        )
    ]
    system_message = message_composer.compose_system_message(question, capbilites)
    assert (
        "KNOW_AND_UNDERSTAND the differences between: variable, instantiation."
        in system_message["content"]
    )
