import pytest
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.multiple_choice_composer.multiple_choice_composer import (
    MultipleChoiceComposer,
)


@pytest.fixture(scope="session")
def multiple_choice_composer() -> MultipleChoiceComposer:
    return MultipleChoiceComposer()


def test_result_template(multiple_choice_composer: MultipleChoiceComposer) -> None:
    result_template = multiple_choice_composer.result_template()
    assert (
        "<result>" in result_template
        and "</result>" in result_template
        and "DISTRACTOR_TEXT_1" in result_template
    )
