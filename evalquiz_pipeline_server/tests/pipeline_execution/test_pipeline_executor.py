from collections import defaultdict
from typing import Any
import pytest
from evalquiz_pipeline_server.pipeline_execution.pipeline import Pipeline
from evalquiz_pipeline_server.pipeline_execution.pipeline_executor import (
    PipelineExecutor,
)
from evalquiz_pipeline_server.pipeline_module_implementations.pipeline_module_implementation import (
    PipelineModuleImplementation,
)
from evalquiz_proto.shared.generated import PipelineModule


@pytest.fixture(scope="session")
def pipeline_executor() -> PipelineExecutor:
    pipeline_executor = PipelineExecutor()
    return pipeline_executor


def test_validate_implementation_for_pipeline(
    pipeline_executor: PipelineExecutor,
) -> None:
    class TestPipelineModuleImplementation(PipelineModuleImplementation):
        def run(input: Any) -> Any:
            raise NotImplementedError()

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
            "a": TestPipelineModuleImplementation(test_pipeline_modules[0], split=True),
            "b": TestPipelineModuleImplementation(test_pipeline_modules[0]),
            "c": TestPipelineModuleImplementation(test_pipeline_modules[0], merge=True),
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
        == True
    )
