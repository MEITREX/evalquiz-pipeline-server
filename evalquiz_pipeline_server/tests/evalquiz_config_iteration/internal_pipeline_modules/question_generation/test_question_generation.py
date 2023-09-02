import pytest
from evalquiz_pipeline_server.evalquiz_config_iteration.default_internal_config import (
    DefaultInternalConfig,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_generation import (
    QuestionGeneration,
)
from evalquiz_proto.shared.generated import Batch, InternalConfig


@pytest.fixture
def question_generation() -> QuestionGeneration:
    question_generation = QuestionGeneration()
    return question_generation


@pytest.mark.asyncio
async def test_run(question_generation: QuestionGeneration) -> None:
    input: tuple[InternalConfig, list[str]] = (DefaultInternalConfig(), [""])
    input[0].batches.append(Batch())
    # output = await question_generation.run(input)
    # output
