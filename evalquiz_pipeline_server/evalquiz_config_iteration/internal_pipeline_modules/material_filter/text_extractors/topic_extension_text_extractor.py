from typing import Any, List, Optional, Tuple, Callable
import random
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.text_extractors.text_extractor import (
    TextExtractor,
)
from evalquiz_proto.shared.generated import Capability
import gensim
import nltk

nltk.download("punkt")


class TopicExtensionTextExtractor(TextExtractor):
    def __init__(
        self,
        max_tokens: int,
        encode_function: Callable[[str], Any],
        max_keywords: Optional[int] = None,
    ):
        super().__init__(max_tokens)
        self.max_keywords = max_keywords
        self.encode_function = encode_function

    def extract_with_capabilites(
        self, texts: List[str], capabilites: List[Capability]
    ) -> str:
        random.shuffle(texts)
        preprocessed_texts = [gensim.utils.simple_preprocess(text) for text in texts]
        model = gensim.models.Word2Vec(preprocessed_texts, min_count=1)
        most_similar_words_of_capabilites: dict[str, List[Tuple[str, float]]] = {}
        for capability in capabilites:
            most_similar_words = model.wv.most_similar(
                positive=capability.keywords, topn=5
            )
            serialized_capability = capability.to_json()
            most_similar_words_of_capabilites[
                serialized_capability
            ] = most_similar_words
        sentences = nltk.sent_tokenize(" ".join(texts))
        keywords = self.compose_keywords(most_similar_words_of_capabilites)
        keyword_sentences = self.find_sentences_with_keywords(sentences, keywords)
        truncated_keyword_sentences = self.sentences_to_max_token_length(
            keyword_sentences
        )
        return " ".join(truncated_keyword_sentences)

    def find_sentences_with_keywords(
        self, sentences: list[str], keywords: list[str]
    ) -> list[str]:
        filtered_sentences: list[str] = []
        for keyword in keywords:
            for sentence in sentences:
                if keyword in sentence:
                    filtered_sentences.append(sentence)
                    break
        return filtered_sentences

    def sentences_to_max_token_length(self, sentences: list[str]) -> list[str]:
        tokens = 0
        filtered_sentences: list[str] = []
        for sentence in sentences:
            encoded_sentence = self.encode_function(sentence)
            tokens += len(encoded_sentence)
            if tokens > self.max_tokens:
                break
            filtered_sentences.append(sentence)
        return filtered_sentences

    def compose_keywords(
        self,
        most_similar_words_of_capabilites: dict[str, List[Tuple[str, float]]],
    ) -> List[str]:
        keywords: list[str] = []
        for serialized_capability in most_similar_words_of_capabilites.keys():
            capability = Capability().from_json(serialized_capability)
            keywords.extend(capability.keywords)
        ranked_similar_probability_word_pairs: List[Tuple[str, float]] = []
        for probability_word_pairs in most_similar_words_of_capabilites.values():
            ranked_similar_probability_word_pairs.extend(probability_word_pairs)
        ranked_similar_probability_word_pairs.sort(
            key=lambda probability_word_pair: probability_word_pair[1]
        )
        ranked_similar_words = [
            probability_word_pair[0]
            for probability_word_pair in ranked_similar_probability_word_pairs
        ]
        keywords.extend(ranked_similar_words)
        if self.max_keywords is not None:
            return keywords[: self.max_keywords]
        return keywords
