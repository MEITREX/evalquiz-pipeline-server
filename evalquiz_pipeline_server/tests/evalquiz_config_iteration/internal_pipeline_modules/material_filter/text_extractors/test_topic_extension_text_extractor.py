import pytest
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.text_extractors.topic_extension_text_extractor import (
    TopicExtensionTextExtractor,
)
import tiktoken

from evalquiz_proto.shared.generated import (
    Capability,
    EducationalObjective,
    Relationship,
)


@pytest.fixture(scope="session")
def text_extractor() -> TopicExtensionTextExtractor:
    encode_function = tiktoken.encoding_for_model("gpt-4")
    text_extractor = TopicExtensionTextExtractor(1000, encode_function.encode)
    return text_extractor


def test_extract_whole_text(text_extractor: TopicExtensionTextExtractor) -> None:
    texts = [
        "This is a simple example for extracting a whole text.",
        "This is another sentence in another file.",
    ]
    capabilites = [
        Capability(
            ["text", "file"],
            EducationalObjective.KNOW_AND_UNDERSTAND,
            Relationship.SIMILARITY,
        )
    ]
    extracted_text = text_extractor.extract_with_capabilites(texts, capabilites)
    assert extracted_text == " ".join(texts) or " ".join(reversed(texts))


texts_to_truncate = [
    (
        [
            "This is a simple example for extracting a whole text.",
            "This is another sentence in another file.",
        ],
        "This is a simple example for extracting a whole text.",
    ),
    (
        [
            "This is another sentence in another file.",
            "This is a simple example for extracting a whole text.",
        ],
        "This is a simple example for extracting a whole text.",
    ),
    (
        [
            "This is a simple example for extracting a whole text. This is another sentence in another file.",
        ],
        "This is a simple example for extracting a whole text.",
    ),
    (
        [
            "This is another sentence in another file. This is a simple example for extracting a whole text.",
        ],
        "This is a simple example for extracting a whole text.",
    ),
    (
        [
            "This is another sentence in another file.",
            "This is another sentence in another file.",
            "This is another sentence in another file.",
            "This is a simple example for extracting a whole text.",
            "This is a simple example for extracting a whole text.",
            "This is a simple example for extracting a whole text.",
        ],
        "This is a simple example for extracting a whole text.",
    ),
    (
        [
            "This is another sentence in another file. This is another sentence in another file. This is another sentence in another file. This is a simple example for extracting a whole text. This is a simple example for extracting a whole text. This is a simple example for extracting a whole text.",
        ],
        "This is a simple example for extracting a whole text.",
    ),
]


@pytest.mark.parametrize("texts, text_part", texts_to_truncate)
def test_extract_text_part(
    text_extractor: TopicExtensionTextExtractor, texts: list[str], text_part: str
) -> None:
    text_extractor.max_keywords = 1
    capabilites = [
        Capability(
            ["text"],
            EducationalObjective.KNOW_AND_UNDERSTAND,
            Relationship.SIMILARITY,
        )
    ]
    extracted_text = text_extractor.extract_with_capabilites(texts, capabilites)
    assert extracted_text == text_part


@pytest.mark.parametrize("texts, text_part", texts_to_truncate)
def test_truncate_text(
    text_extractor: TopicExtensionTextExtractor, texts: list[str], text_part: str
) -> None:
    text_extractor.max_tokens = 12
    capabilites = [
        Capability(
            ["text"],
            EducationalObjective.KNOW_AND_UNDERSTAND,
            Relationship.SIMILARITY,
        )
    ]
    extracted_text = text_extractor.extract_with_capabilites(texts, capabilites)
    assert extracted_text == text_part
