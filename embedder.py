from sentence_transformers import SentenceTransformer
from typing import List


# Load the embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(EMBEDDING_MODEL)


def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """Embeds document chunks using a local Sentence Transformer model."""

    embeddings = model.encode(
        chunks,
        normalize_embeddings=True
    )

    embeddings = embeddings.tolist()

    print(f"Embedded {len(embeddings)} chunks.")
    print(f"Embedding dimension: {len(embeddings[0])}")

    return embeddings


def embed_User_query(query: str) -> List[float]:
    """Embeds a user query using the local Sentence Transformer model."""

    embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    return embedding.tolist()