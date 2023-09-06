from typing import Any, Optional, Callable
import random
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.text_extractors.text_extractor import (
    TextExtractor,
)
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.text_extractors.topic_extension_text_extractor import (
    TopicExtensionTextExtractor,
)
from evalquiz_proto.shared.generated import Capability
import gensim
import nltk
from top2vec import Top2Vec

nltk.download("punkt")


class Top2VecExtensionTextExtractor(TopicExtensionTextExtractor):
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
        preprocessed_texts = self.preprocess_texts(texts)
        model = Top2Vec(
            preprocessed_texts, embedding_model="universal-sentence-encoder"
        )
        most_similar_words_of_capabilites = (
            self.find_most_similar_words_of_capabilities(
                preprocessed_texts, model, capabilites
            )
        )
        sentences = nltk.sent_tokenize(" ".join(texts))
        keywords = self.compose_keywords(most_similar_words_of_capabilites)
        keyword_sentences = self.find_sentences_with_keywords(sentences, keywords)
        truncated_keyword_sentences = self.sentences_to_max_token_length(
            keyword_sentences, keywords
        )
        return "\n".join(truncated_keyword_sentences)

    def find_similar_words_in_texts(
        self,
        preprocessed_texts: list[str],
        model: Any,
        keywords: list[str],
        topn: int = 5,
    ) -> list[tuple[str, float]]:
        word_similarity_pairs: list[tuple[str, float]] = []
        for word in preprocessed_texts:
            similarity = model.model.n_similarity([word], keywords)
            word_similarity_pairs.append((word, similarity))
        most_similar_words = sorted(word_similarity_pairs, key=lambda x: x[1])
        return most_similar_words[:topn]
