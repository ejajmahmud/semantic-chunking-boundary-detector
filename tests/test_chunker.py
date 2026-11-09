"""Unit tests for semantic-chunking-boundary-detector."""
import unittest
from semantic_chunking_boundary_detector.chunker import SemanticChunker


class TestSemanticChunker(unittest.TestCase):
    def setUp(self):
        self.chunker = SemanticChunker(min_words=5, max_words=30)

    def test_semantic_split_on_distinct_topic(self):
        doc = (
            "Kubernetes orchestrates Docker container clusters efficiently and manages service discovery. "
            "Deep sea cephalopods possess remarkable camouflage capabilities in the ocean."
        )
        chunks = self.chunker.chunk_document(doc)
        self.assertEqual(len(chunks), 2)
