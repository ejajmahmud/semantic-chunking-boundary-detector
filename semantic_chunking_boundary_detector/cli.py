"""CLI for semantic-chunking-boundary-detector."""
import sys
import argparse
from .chunker import SemanticChunker


def main():
    parser = argparse.ArgumentParser(description="Semantic Chunking Boundary Detector CLI")
    parser.add_argument("--demo", action="store_true", help="Run semantic chunking demo")
    args = parser.parse_args()

    if args.demo:
        chunker = SemanticChunker(min_words=10, max_words=50)
        doc = (
            "PostgreSQL is an open-source relational database management system. "
            "It emphasizes extensibility and SQL compliance with ACID transactional guarantees. "
            "Now let us talk about cooking delicious pasta. "
            "To boil pasta correctly, bring a large pot of salted water to a rolling boil."
        )
        chunks = chunker.chunk_document(doc)
        print(f"Generated {len(chunks)} Semantic Chunks:")
        for c in chunks:
            print(f"  Chunk #{c.chunk_id} ({c.word_count} words): {c.text}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
