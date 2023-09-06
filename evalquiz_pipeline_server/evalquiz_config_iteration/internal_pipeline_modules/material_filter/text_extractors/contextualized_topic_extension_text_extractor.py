import random
from typing import Callable, Optional, Any
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.text_extractors.topic_extension_text_extractor import (
    TopicExtensionTextExtractor,
)
from evalquiz_proto.shared.generated import Capability
from contextualized_topic_models.models.ctm import ZeroShotTM
from contextualized_topic_models.utils.data_preparation import TopicModelDataPreparation
from contextualized_topic_models.utils.data_preparation import bert_embeddings_from_file
import nltk


class ContextualizedTopicExtensionTextExtractor(TopicExtensionTextExtractor):
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
        data_preparation = TopicModelDataPreparation(
            "paraphrase-multilingual-mpnet-base-v2"
        )
        training_dataset = data_preparation.fit(
            text_for_contextual=texts, text_for_bow=preprocessed_texts
        )
        model = ZeroShotTM(
            bow_size=len(data_preparation.vocab), contextual_size=768, n_components=50
        )
        model.fit(training_dataset)
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