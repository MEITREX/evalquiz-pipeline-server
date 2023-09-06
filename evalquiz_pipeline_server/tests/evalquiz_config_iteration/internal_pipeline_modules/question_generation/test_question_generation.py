import pytest
from evalquiz_pipeline_server.tests.evalquiz_config_iteration.internal_pipeline_modules.material_filter.test_material_filter import (
    internal_lecture_material,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.default_internal_config import (
    DefaultInternalConfig,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_generation import (
    QuestionGeneration,
)
from evalquiz_proto.shared.generated import (
    Batch,
    Capability,
    EducationalObjective,
    InternalConfig,
    Question,
    QuestionType,
    Relationship,
    LectureMaterial,
)


@pytest.fixture(scope="session")
def question_generation() -> QuestionGeneration:
    question_generation = QuestionGeneration()
    return question_generation


@pytest.fixture(scope="session")
def internal_config() -> InternalConfig:
    internal_config = DefaultInternalConfig()
    internal_config.batches.append(
        Batch(
            [
                LectureMaterial(
                    "Example material",
                    None,
                    "PLACEHOLDER",
                    "text/markdown",
                )
            ],
            [Question(QuestionType.MULTIPLE_CHOICE)],
            [
                Capability(
                    ["categorical", "numerical"],
                    EducationalObjective.KNOW_AND_UNDERSTAND,
                    Relationship.DIFFERENCES,
                )
            ],
        )
    )
    return internal_config


@pytest.fixture(scope="session")
def filtered_text() -> str:
    """Source: An Introduction to Statistical Learning with Applications in R Second Edition"""
    return """Variables can be characterized as either quantitative or qualitative (also
known as categorical). Quantitative variables take on numerical values.
Examples include a person’s age, height, or income, the value of a house,
and the price of a stock. In contrast, qualitative variables take on values
in one of K diﬀerent classes, or categories. Examples of qualitative vari-
ables include a person’s marital status (married or not), the brand of prod-
uct purchased (brand A, B, or C), whether a person defaults on a debt
(yes or no), or a cancer diagnosis (Acute Myelogenous Leukemia, Acute
Lymphoblastic Leukemia, or No Leukemia). We tend to refer to problems
with a quantitative response as regression problems, while those involv-
ing a qualitative response are often referred to as classification problems.
However, the distinction is not always that crisp. Least squares linear re-
gression (Chapter 3) is used with a quantitative response, whereas logistic
regression (Chapter 4) is typically used with a qualitative (two-class, or
binary) response. Thus, despite its name, logistic regression is a classifica-
tion method. But since it estimates class probabilities, it can be thought of
as a regression method as well. Some statistical methods, such as K-nearest
neighbors (Chapters 2 and 4) and boosting (Chapter 8), can be used in the
case of either quantitative or qualitative responses.
We tend to select statistical learning methods on the basis of whether
the response is quantitative or qualitative; i.e. we might use linear regres-
sion when quantitative and logistic regression when qualitative. However,
whether the predictors are qualitative or quantitative is generally consid-
ered less important. Most of the statistical learning methods discussed in
this book can be applied regardless of the predictor variable type, provided
that any qualitative predictors are properly coded before the analysis is
performed. This is discussed in Chapter 3.
"""


@pytest.mark.asyncio
async def test_run(
    question_generation: QuestionGeneration,
    internal_config: InternalConfig,
    filtered_text: str,
) -> None:
    """
    output = MultipleChoice(
        question_text = 'Are categorical variables only utilized in classification problems?',
        answer_text = 'No, they can be used in both regression and classification problems if properly coded.',
        distractor_text = [
            'Yes, categorical variables can only be used in classification problems.',
            'No, categorical variables cannot not used in either classification or regression problems.'
        ]
    )
    """
    input: tuple[InternalConfig, list[str]] = (internal_config, [filtered_text])
    output = await question_generation.run(input)
    pass
