import random
from typing import Callable, Optional, Any
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.text_extractors.topic_extension_text_extractor import (
    TopicExtensionTextExtractor,
)
from evalquiz_proto.shared.generated import Capability
from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups
import nltk


class BertopicExtensionTextExtractor(TopicExtensionTextExtractor):
    def __init__(
        self,
        max_tokens: int,
        encode_function: Callable[[str], Any],
        max_keywords: Optional[int] = None,
    ):
        super().__init__(max_tokens, encode_function, max_keywords)

    def extract_with_capabilites(
        self, texts: list[str], capabilites: list[Capability]
    ) -> str:
        random.shuffle(texts)
        training_docs = fetch_20newsgroups(subset='all',  remove=('headers', 'footers', 'quotes'))['data']
        model = BERTopic(language="english", calculate_probabilities=True, verbose=True)
        model.fit(training_docs)
        most_similar_words_of_capabilites = (
            self.find_most_similar_words_of_capabilities(model, capabilites)
        )
        sentences = nltk.sent_tokenize(" ".join(texts))
        keywords = self.compose_keywords(most_similar_words_of_capabilites)
        keyword_sentences = self.find_sentences_with_keywords(sentences, keywords)
        truncated_keyword_sentences = self.sentences_to_max_token_length(
            keyword_sentences, keywords
        )
        return "\n".join(truncated_keyword_sentences)

    def find_most_similar_words_of_capabilities(
        self, model: BERTopic, capabilites: list[Capability]
    ) -> dict[str, list[tuple[str, float]]]:
        most_similar_words_of_capabilites: dict[str, list[tuple[str, float]]] = {}
        for capability in capabilites:
            search_term = " ".join(capability.keywords)
            most_similar_words = model.find_topics(search_term, top_n=5)
            serialized_capability = capability.to_json()
            most_similar_words_of_capabilites[
                serialized_capability
            ] = most_similar_words
        return most_similar_words_of_capabilites
