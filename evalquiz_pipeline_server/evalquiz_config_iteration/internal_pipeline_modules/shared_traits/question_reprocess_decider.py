from typing import Any, Callable

import betterproto

from evalquiz_proto.shared.generated import ByMetrics, Mode, Question


class QuestionReprocessDecider:
    def __init__(self) -> None:
        self.metric_evaluators: dict[str, Callable[[Any, Any], Any]] = {
            "eq": lambda x, y: x == y,
            "neq": lambda x, y: x != y,
            "geq": lambda x, y: x >= y,
            "leq": lambda x, y: x <= y,
            "ge": lambda x, y: x > y,
            "le": lambda x, y: x < y,
            "is": lambda x, y: x is y,
            "is not": lambda x, y: x is not y,
            "in": lambda x, y: x in y,
            "part_of": lambda x, y: y in x,
        }

    def is_question_to_reprocess(self, question: Question, mode: Mode) -> bool:
        (type, mode_value) = betterproto.which_one_of(mode, "mode")
        match type:
            case "complete":
                return True
            case "by_metrics":
                if mode_value is None or not isinstance(mode_value, ByMetrics):
                    raise ValueError("ByMetrics object was not instantiated correctly.")
                if (
                    question.evaluation_results is not None
                    and mode_value.evaluation_reference
                    in question.evaluation_results.keys()
                ):
                    return self.run_metric_evaluator(question, mode_value)
                return False
            case _:
                return question.generation_result is None

    def run_metric_evaluator(self, question: Question, by_metrics: ByMetrics) -> bool:
        metric_evaluator = self.metric_evaluators[by_metrics.evaluator_type]
        question_evaluation_result = question.evaluation_results[
            by_metrics.evaluation_reference
        ]
        (_, question_evaluation_result_value) = betterproto.which_one_of(
            question_evaluation_result, "evaluation_result"
        )
        (_, by_metrics_evaluation_result) = betterproto.which_one_of(
            by_metrics.evaluation_result, "evaluation_result"
        )
        return metric_evaluator(
            question_evaluation_result_value,
            by_metrics_evaluation_result,
        )
