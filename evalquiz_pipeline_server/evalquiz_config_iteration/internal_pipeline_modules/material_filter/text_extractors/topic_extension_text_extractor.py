from pathlib import Path
from typing import Any, Optional, Callable
import random
from evalquiz_pipeline_server.evalquiz_config_iteration.internal_pipeline_modules.material_filter.text_extractors.text_extractor import (
    TextExtractor,
)
from evalquiz_proto.shared.generated import Capability
import gensim
import nltk
import pypandoc

nltk.download("punkt")
from datasets import load_dataset


class TopicExtensionTextExtractor(TextExtractor):
    def __init__(
        self,
        max_tokens: int,
        encode_function: Callable[[str], Any],
        model_path: Path = Path(__file__).parent / "arxiv_papers.model",
        max_keywords: Optional[int] = None,
    ):
        super().__init__(max_tokens)
        self.model_path = model_path
        self.max_keywords = max_keywords
        self.encode_function = encode_function

    def extract_with_capabilites(
        self, texts: list[str], capabilites: list[Capability]
    ) -> str:
        random.shuffle(texts)
        preprocessed_texts = self.preprocess_texts(texts)
        model = gensim.models.Word2Vec.load(str(self.model_path))
        model.min_count = 1
        model.build_vocab(preprocessed_texts, update=True)
        total_words = len(model.wv.index_to_key)
        model.train(preprocessed_texts, total_words=total_words, epochs=model.epochs)
        most_similar_words_of_capabilites = (
            self.find_most_similar_words_of_capabilities(
                preprocessed_texts, model.wv, capabilites
            )
        )
        sentences = nltk.sent_tokenize(" ".join(texts))
        keywords = self.compose_keywords(most_similar_words_of_capabilites)
        keyword_sentences = self.find_sentences_with_keywords(sentences, keywords)
        truncated_keyword_sentences = self.sentences_to_max_token_length(
            keyword_sentences, keywords
        )
        return "\n".join(truncated_keyword_sentences)

    def preprocess_texts(self, texts: list[str]) -> list[list[str]]:
        plain_texts = [
            pypandoc.convert_text(text, "plain", format="markdown") for text in texts
        ]
        return [
            gensim.utils.simple_preprocess(plain_text) for plain_text in plain_texts
        ]

    def find_most_similar_words_of_capabilities(
        self,
        preprocessed_texts: list[list[str]],
        model: Any,
        capabilites: list[Capability],
    ) -> dict[str, list[tuple[str, float]]]:
        most_similar_words_of_capabilites: dict[str, list[tuple[str, float]]] = {}
        for capability in capabilites:
            most_similar_words = self.find_similar_words_in_texts(
                preprocessed_texts,
                model,
                capability.keywords,
            )
            serialized_capability = capability.to_json(include_default_values=True)
            most_similar_words_of_capabilites[
                serialized_capability
            ] = most_similar_words
        return most_similar_words_of_capabilites

    def find_similar_words_in_texts(
        self,
        preprocessed_texts: list[list[str]],
        keyed_vectors: gensim.models.KeyedVectors,
        keywords: list[str],
        topn: int = 5,
    ) -> list[tuple[str, float]]:
        word_similarity_pairs: list[tuple[str, float]] = []
        bag_of_words: set[str] = self.bag_of_words_from_preprocessed_texts(
            preprocessed_texts
        )
        keywords_length = len(keywords)
        for word in bag_of_words:
            similarity = keyed_vectors.n_similarity([word], keywords)
            word_similarity_pairs.append((word, similarity))
        most_similar_words = sorted(
            word_similarity_pairs,
            key=lambda word_similarity_pair: -word_similarity_pair[1],
        )
        return most_similar_words[keywords_length:topn]

    def bag_of_words_from_preprocessed_texts(
        self, preprocessed_texts: list[list[str]]
    ) -> set[str]:
        bag_of_words: set[str] = set()
        for preprocessed_text in preprocessed_texts:
            unique_preprocessed_text = set(preprocessed_text)
            bag_of_words = bag_of_words.union(unique_preprocessed_text)
        return bag_of_words

    def find_sentences_with_keywords(
        self, sentences: list[str], keywords: list[str]
    ) -> list[str]:
        filtered_sentences: list[str] = []
        for sentence in sentences:
            for keyword in keywords:
                if (
                    keyword in sentence or keyword.capitalize() in sentence
                ) and sentence not in filtered_sentences:
                    filtered_sentences.append(sentence)
                    break
        return filtered_sentences

    def sentences_to_max_token_length(
        self, sentences: list[str], keywords: list[str]
    ) -> list[str]:
        tokens = 0
        filtered_sentences: dict[int, str] = {}
        for keyword in keywords:
            for i, sentence in enumerate(sentences):
                if (
                    keyword in sentence or keyword.capitalize() in sentence
                ) and sentence not in filtered_sentences.values():
                    encoded_sentence = self.encode_function(sentence)
                    tokens += len(encoded_sentence)
                    if tokens > self.max_tokens:
                        break
                    filtered_sentences[i] = sentence
        sorted_filtered_sentences = sorted(
            filtered_sentences.items(), key=lambda x: x[0]
        )
        sorted_filtered_sentences_list = [
            sentence for _, sentence in sorted_filtered_sentences
        ]
        return sorted_filtered_sentences_list

    def compose_keywords(
        self,
        most_similar_words_of_capabilites: dict[str, list[tuple[str, float]]],
    ) -> list[str]:
        keywords: list[str] = []
        for serialized_capability in most_similar_words_of_capabilites.keys():
            capability = Capability().from_json(serialized_capability)
            keywords.extend(capability.keywords)
        ranked_similar_probability_word_pairs: list[tuple[str, float]] = []
        for probability_word_pairs in most_similar_words_of_capabilites.values():
            ranked_similar_probability_word_pairs.extend(probability_word_pairs)
        ranked_similar_probability_word_pairs.sort(
            key=lambda probability_word_pair: -probability_word_pair[1]
        )
        ranked_similar_words = [
            probability_word_pair[0]
            for probability_word_pair in ranked_similar_probability_word_pairs
        ]
        keywords.extend(ranked_similar_words)
        if self.max_keywords is not None:
            return keywords[: self.max_keywords]
        return keywords

    def _train_model(self) -> None:
        arxiv_papers = load_dataset("CShorten/ML-ArXiv-Papers", split="train")
        abstracts = arxiv_papers["abstract"]
        preprocessed_abstracts = self.preprocess_texts(abstracts)
        model = gensim.models.Word2Vec(preprocessed_abstracts)
        model.save(self.model_path)
