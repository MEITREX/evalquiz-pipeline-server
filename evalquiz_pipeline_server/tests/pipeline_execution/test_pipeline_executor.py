from typing import Any, Tuple
import pytest
from evalquiz_pipeline_server.exceptions import (
    PipelineModuleCompositionNotValidException,
)
from evalquiz_pipeline_server.pipeline_execution.pipeline import Pipeline
from evalquiz_pipeline_server.pipeline_execution.pipeline_executor import (
    PipelineExecutor,
)
from evalquiz_pipeline_server.pipeline_module_implementations.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import PipelineModule


class TestPipelineModuleImplementation(InternalPipelineModule):
    def run(self, input: Any) -> Any:
        raise NotImplementedError()


@pytest.fixture(scope="session")
def pipeline_executor() -> PipelineExecutor:
    pipeline_executor = PipelineExecutor()
    return pipeline_executor


"""Describes test cases when implementation validation should fail and pass.
First element: tuple of booleans: Split configurations: (a_split, b_split, c_split)
Second element: tuple booleans: Merge configurations: (a_merge, b_merge, c_merge)
Third element: bool: The expected outcoming validate_implementation_for_pipeline() boolean.
"""
split_merge_configurations = [
    ((True, False, False), (False, False, True), True),
    ((False, False, False), (False, False, False), True),
    ((False, False, False), (True, False, False), False),
    ((True, True, False), (False, False, False), False),
    ((True, True, False), (True, False, True), True),
]


@pytest.mark.parametrize(
    "split_configurations, merge_configurations, expected", split_merge_configurations
)
def test_validate_implementation_for_pipeline(
    split_configurations: Tuple[bool, bool, bool],
    merge_configurations: Tuple[bool, bool, bool],
    expected: bool,
) -> None:
    (a_split, b_split, c_split) = split_configurations
    (a_merge, b_merge, c_merge) = merge_configurations
    test_pipeline_modules: list[InternalPipelineModule] = [
        TestPipelineModuleImplementation(
            PipelineModule("a", "str", "str"), split=a_split, merge=a_merge
        ),
        TestPipelineModuleImplementation(
            PipelineModule("b", "str", "int"), split=b_split, merge=b_merge
        ),
        TestPipelineModuleImplementation(
            PipelineModule("c", "int", "Any"), split=c_split, merge=c_merge
        ),
    ]
    if expected == False:
        with pytest.raises(PipelineModuleCompositionNotValidException):
            Pipeline("test_pipeline", test_pipeline_modules)
    else:
        Pipeline("test_pipeline", test_pipeline_modules)
