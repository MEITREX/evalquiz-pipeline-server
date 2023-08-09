from collections import defaultdict
from typing import Any, Tuple
import pytest
from evalquiz_pipeline_server.pipeline_execution.pipeline import Pipeline
from evalquiz_pipeline_server.pipeline_execution.pipeline_executor import (
    PipelineExecutor,
)
from evalquiz_pipeline_server.pipeline_module_implementations.pipeline_module_implementation import (
    PipelineModuleImplementation,
)
from evalquiz_proto.shared.generated import PipelineModule


class TestPipelineModuleImplementation(PipelineModuleImplementation):
    def run(input: Any) -> Any:
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
    test_pipeline_modules = [
        PipelineModule("a", "str", "str"),
        PipelineModule("b", "str", "int"),
        PipelineModule("c", "int", "Any"),
    ]
    test_pipeline = Pipeline("test_pipeline", test_pipeline_modules)
    test_pipeline_module_implementations: defaultdict[
        "str", PipelineModuleImplementation
    ] = defaultdict(
        None,
        {
            "a": TestPipelineModuleImplementation(
                test_pipeline_modules[0], split=a_split, merge=a_merge
            ),
            "b": TestPipelineModuleImplementation(
                test_pipeline_modules[0], split=b_split, merge=b_merge
            ),
            "c": TestPipelineModuleImplementation(
                test_pipeline_modules[0], split=c_split, merge=c_merge
            ),
        },
    )
    test_pipeline_dict: defaultdict["str", Pipeline] = defaultdict(
        None, {test_pipeline.reference: test_pipeline}
    )
    pipeline_executor = PipelineExecutor(
        test_pipeline_dict, test_pipeline_module_implementations
    )
    assert (
        pipeline_executor.validate_implementation_for_pipeline(test_pipeline.reference)
        == expected
    )
