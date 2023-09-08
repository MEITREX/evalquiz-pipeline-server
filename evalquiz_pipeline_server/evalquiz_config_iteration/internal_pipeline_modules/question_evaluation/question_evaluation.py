from typing import Any

import betterproto
from evalquiz_pipeline_server.evalquiz_config_iteration.default_internal_config import (
    DefaultInternalConfig,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.internal_evaluations.internal_evaluation import InternalEvaluation
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_evaluation.internal_evaluations.internal_language_model_evaluation import InternalLanguageModelEvaluation
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.shared_traits.question_reprocess_decider import (
    QuestionReprocessDecider,
)
from evalquiz_pipeline_server.pipeline_execution.internal_pipeline_module import (
    InternalPipelineModule,
)
from evalquiz_proto.shared.generated import (
    Batch,
    Complete,
    EvaluationSettings,
    Evaluation,
    InternalConfig,
    Metric,
    Mode,
    PipelineModule,
)


class QuestionEvaluation(InternalPipelineModule, QuestionReprocessDecider):
    def __init__(self) -> None:
        pipeline_module = PipelineModule(
            "question_evaluation", "InternalConfig", "InternalConfig"
        )
        super().__init__(pipeline_module)
        self.default_internal_config = DefaultInternalConfig()
        self.internal_evaluations = {
            "language_model_evaluation": InternalLanguageModelEvaluation()
        }

    async def run(self, input: Any) -> Any:
        if not isinstance(input, InternalConfig):
            raise TypeError()
        evaluation_settings = self.resolve_evaluation_settings(input)
        for batch in input.batches:
            self.process_batch(batch, evaluation_settings.metrics)

    def resolve_evaluation_settings(
        self, internal_config: InternalConfig
    ) -> EvaluationSettings:
        if internal_config.evaluation_settings is not None:
            return internal_config.evaluation_settings
        elif self.default_internal_config.evaluation_settings is not None:
            return self.default_internal_config.evaluation_settings
        else:
            raise ValueError("DefaultInternalConfig not specified correctly.")

    def process_batch(self, batch: Batch, metrics: list[Metric]) -> None:
        for question in batch.question_to_generate:
            for metric in metrics:
                mode = metric.mode or Mode(complete=Complete())
                if self.is_question_to_reprocess(question, mode):
                    (type, evaluation) = betterproto.which_one_of(metric.evaluation, "evaluation")
                    if evaluation is None:
                        raise ValueError("Evaluation was not instantiated correctly.")
                    internal_evaluation = self.internal_evaluations[type]
                    question.evaluations[metric.reference] = internal_evaluation.evaluate(metric.evaluation)