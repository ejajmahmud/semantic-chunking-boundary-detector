"""Core Semantic Chunking Boundary Detector implementation."""
import re
from typing import Dict, List, Set, Optional, Tuple, Any


class DocumentChunk:
    def __init__(self, chunk_id: int, text: str, word_count: int):
        self.chunk_id = chunk_id
        self.text = text
        self.word_count = word_count


class SemanticChunker:
    def __init__(self, min_words: int = 20, max_words: int = 150):
        self.min_words = min_words
        self.max_words = max_words
        self.sentence_regex = re.compile(r"(?<=[.!?])\s+")

    def _get_words_set(self, sentence: str) -> Set[str]:
        return set(re.findall(r"\b[a-zA-Z]{3,}\b", sentence.lower()))

    def chunk_document(self, text: str) -> List[DocumentChunk]:
        raw_sentences = [s.strip() for s in self.sentence_regex.split(text) if s.strip()]
        if not raw_sentences:
            return []

        chunks: List[DocumentChunk] = []
        current_sentences: List[str] = [raw_sentences[0]]
        current_word_count = len(raw_sentences[0].split())

        for i in range(1, len(raw_sentences)):
            sent = raw_sentences[i]
            sent_word_count = len(sent.split())

            # Compute lexical similarity between previous sentence and current
            prev_words = self._get_words_set(raw_sentences[i - 1])
            curr_words = self._get_words_set(sent)
            intersection = prev_words.intersection(curr_words)
            union = prev_words.union(curr_words)
            jaccard = len(intersection) / max(1, len(union))

            # Split condition: jaccard is very low (topic shift) AND we have exceeded min_words,
            # OR we are about to exceed max_words
            should_split = (jaccard < 0.10 and current_word_count >= self.min_words) or (current_word_count + sent_word_count > self.max_words)

            if should_split:
                chunk_text = " ".join(current_sentences)
                chunks.append(DocumentChunk(len(chunks) + 1, chunk_text, current_word_count))
                current_sentences = [sent]
                current_word_count = sent_word_count
            else:
                current_sentences.append(sent)
                current_word_count += sent_word_count

        if current_sentences:
            chunk_text = " ".join(current_sentences)
            chunks.append(DocumentChunk(len(chunks) + 1, chunk_text, current_word_count))

        return chunks
