from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.multiple_choice_composer.multiple_choice_few_shot_examples import (
    few_shot_example_filtered_text_1, few_shot_example_filtered_text_2
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.few_shot_example import (
    FewShotExample,
)
from evalquiz_proto.shared.generated import (
    Capability,
    EducationalObjective,
    MultipleResponse,
    Question,
    QuestionType,
    Relationship,
    GenerationResult,
)

few_shot_example_1 = FewShotExample(
    Question(QuestionType.MULTIPLE_RESPONSE, evaluation_results={}),
    [
        Capability(
            ["scrum", "master"],
            EducationalObjective.KNOW_AND_UNDERSTAND,
            Relationship.COMPLEX,
        )
    ],
    few_shot_example_filtered_text_1,
    GenerationResult(
        multiple_response=MultipleResponse(
            "Which of the following is true about the Scrum Master?",
            [
                "The Scrum Master is part of the Scrum Team.",
                "The Scrum Master can participate as a developer.",
            ],
            [
                "The Scrum Master is not accountable for the Scrum Team’s effectiveness.",
                "The Scrum Master develops how the product should look like.",
            ],
        )
    ),
)

few_shot_example_2 = FewShotExample(
    Question(QuestionType.MULTIPLE_RESPONSE, evaluation_results={}),
    [
        Capability(
            ["product", "owner"],
            EducationalObjective.KNOW_AND_UNDERSTAND,
            Relationship.COMPLEX,
        )
    ],
    few_shot_example_filtered_text_2,
    GenerationResult(
        multiple_response=MultipleResponse(
            "What is a responsibility of the Product Owner?",
            [
                "Maximize the value of the product.",
                "Ensure that attendees are prepared to discuss the most important Product Backlog items",
                "Cancel the Sprint if necessary",
            ],
            ["Write most of the implementation code."],
        )
    ),
)

multiple_response_few_shot_examples = [few_shot_example_1, few_shot_example_2]
