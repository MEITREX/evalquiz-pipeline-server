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
    assert extracted_text == " ".join(texts)
