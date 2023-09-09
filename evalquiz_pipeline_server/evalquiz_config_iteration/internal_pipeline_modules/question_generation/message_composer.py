from collections import defaultdict
import tiktoken
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.few_shot_example import (
    FewShotExample,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.multiple_choice_composer.multiple_choice_composer import (
    MultipleChoiceComposer,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.multiple_response_composer import (
    MultipleResponseComposer,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.question_generation.question_type_composer.question_type_composer import (
    QuestionTypeComposer,
)
from evalquiz_proto.shared.generated import (
    Capability,
    CourseSettings,
    Question,
    GenerationSettings,
    QuestionType,
    EducationalObjective,
    Relationship,
)


class MessageComposer:
    def __init__(
        self,
        course_settings: CourseSettings,
        generation_settings: GenerationSettings,
        max_previous_messages: int = 3,
    ) -> None:
        self.course_settings = course_settings
        self.generation_settings = generation_settings
        self.max_previous_messages = max_previous_messages
        self.question_type_composers: dict[QuestionType, QuestionTypeComposer] = {
            QuestionType.MULTIPLE_CHOICE: MultipleChoiceComposer(),
            QuestionType.MULTIPLE_RESPONSE: MultipleResponseComposer(),
        }
        self.educational_objective_explanations: dict[EducationalObjective, str] = {
            EducationalObjective.KNOW_AND_UNDERSTAND: "The student knows and understands the specific concepts.",
            EducationalObjective.APPLY: "The student can apply the specific concepts to examples. Can name examples containing the specific concepts.",
            EducationalObjective.ANALYZE: "The student can analyze settings which contains the specific concepts and identify where these concepts play a role in order to understand the system.",
            EducationalObjective.SYNTHESIZE: "The student can synthesize the specific concepts.",
            EducationalObjective.EVALUATE: "The student can carry out a scientific evaluation of a scenario connected with the specific concepts.",
            EducationalObjective.INNOVATE: "The student can use the specific concepts as a basis to synthesize valuable new concepts.",
        }
        self.relationship_translations: dict[Relationship, str] = {
            Relationship.SIMILARITY: "the similarities between",
            Relationship.DIFFERENCES: "the differences between",
            Relationship.ORDER: "the order of",
            Relationship.COMPLEX: "the complex relationship between",
        }
        self.token_overhead

    def compose(
        self,
        question: Question,
        capabilites: list[Capability],
        filtered_text: str,
        previous_messages: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        return (
            [self.compose_system_message(capabilites)]
            + self.compose_few_shot_examples(question.question_type, previous_messages)
            + [self.compose_query_message(question, capabilites, filtered_text)]
        )

    def compose_system_message(self, capabilites: list[Capability]) -> dict[str, str]:
        return {
            "role": "system",
            "content": """You are a question generation assistant that supports generating questions in multiple fixed formats.

The question generated by you serves the purpose of helping a student to self-assess, which skills they have acquired.

You can assume that the student already has acquired the following skills:
"""
            + self.compose_capability_message(self.course_settings.required_capabilites)
            + """Here is more information about the ALL_CAPS formatted instructions used in the skill descriptions:
"""
            + self.compose_relevant_educational_objective_explanations(capabilites),
        }

    def compose_few_shot_examples(
        self, question_type: QuestionType, previous_messages: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        max_previous_messages_and_responses = self.max_previous_messages * 2
        few_shot_examples = self.question_type_composers[
            question_type
        ].few_shot_examples
        return previous_messages[
            :max_previous_messages_and_responses
        ] + self._compose_few_shot_examples(few_shot_examples)

    def _compose_few_shot_examples(
        self, few_shot_examples: list[FewShotExample]
    ) -> list[dict[str, str]]:
        few_shot_example_messages: list[dict[str, str]] = []
        for few_shot_example in few_shot_examples:
            user_example_message = self.compose_query_message(
                few_shot_example.question,
                few_shot_example.capabilites,
                few_shot_example.filtered_text,
            )
            question_type_composer = self.question_type_composers[
                few_shot_example.question.question_type
            ]
            assistant_example = question_type_composer.result_template(
                few_shot_example.generation_result
            )
            few_shot_example_messages.append(user_example_message)
            few_shot_example_messages.append(
                {"role": "assistant", "content": assistant_example}
            )
        return few_shot_example_messages

    def compose_query_message(
        self, question: Question, capabilities: list[Capability], filtered_text: str
    ) -> dict[str, str]:
        question_type_composer = self.question_type_composers[question.question_type]
        question_type_query_message = question_type_composer.compose_query_message()
        content = (
            """Your goal is to use the given markdown formatted text input to generate a question of the following JSON format:

"""
            + question_type_query_message
            + """Give your answer in the specified JSON format at all cost!

A student who can answer the generated question successfully should have acquired the following skill set:
"""
            + self.compose_capability_message(capabilities)
            + """Double-check that the question supports strengthening the previously given skills.

Markdown formatted text input:
```md
"""
            + filtered_text
            + "```"
        )
        return {"role": "user", "content": content}

    def compose_capability_message(self, capabilites: list[Capability]) -> str:
        capability_message = ""
        for capability in capabilites:
            capability_text = (
                capability.educational_objective.name
                + " "
                + self.relationship_translations[capability.relationship]
                + ": "
                + ", ".join(capability.keywords)
            )
            capability_message += capability_text + ".\n"
        capability_message += "\n"
        return capability_message

    def compose_relevant_educational_objective_explanations(
        self, capabilites: list[Capability]
    ) -> str:
        relevant_educational_objectives = [
            capability.educational_objective for capability in capabilites
        ]
        relevant_educational_objective_explanations = {
            educational_objective: self.educational_objective_explanations[
                educational_objective
            ]
            for educational_objective in relevant_educational_objectives
        }
        objective_explanations_message = ""
        for (
            educational_objective,
            explanation,
        ) in relevant_educational_objective_explanations.items():
            objective_explanations_message += (
                educational_objective.name + ": " + explanation + ".\n"
            )
        objective_explanations_message += "\n"
        return objective_explanations_message

    def collect_few_shot_example_sources(
        self, few_shot_example_sources: defaultdict[int, defaultdict[str, str]]
    ) -> list[defaultdict[str, str]]:
        sorted_few_shot_example_sources = sorted(
            few_shot_example_sources.items(), key=lambda x: x[0]
        )
        sorted_filtered_few_shot_example_sources = [
            example_source for _, example_source in sorted_few_shot_example_sources
        ]
        return sorted_filtered_few_shot_example_sources

    @property
    def token_overhead(self) -> int:
        messages = self.compose(Question(QuestionType.MULTIPLE_CHOICE), [], "", [])
        return self.num_tokens_from_messages(messages)

    def num_tokens_from_messages(
        self, messages: list[dict[str, str]], model: str = "gpt-3.5-turbo-0301"
    ) -> int:
        """Source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions, Accessed: 03.09.2023
        Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError()
