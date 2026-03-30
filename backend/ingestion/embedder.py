"""
Ingestion: Embedder.

Generates dense vector embeddings for text chunks using the configured
embedding model (OpenAI or Nomic via Ollama).
"""

from __future__ import annotations

from typing import Any


class TextEmbedder:
    """
    Generates text embeddings for document chunks using a configurable
    embedding model.

    Supports OpenAI ``text-embedding-ada-002`` and Nomic ``nomic-embed-text``
    (via Ollama for local inference).

    Typical usage:
        embedder = TextEmbedder(model="text-embedding-ada-002")
        embeddings = embedder.embed(chunks)
    """

    def __init__(self, model: str = "text-embedding-ada-002", client: Any = None) -> None:
        """
        Args:
            model: Embedding model identifier.
            client: Optional pre-initialised embedding client.
        """
        self.model = model
        self.client = client

    def embed(self, chunks: list[dict]) -> list[dict]:
        """
        Generate embeddings for a list of text chunks.

        Args:
            chunks: List of chunk dicts from :class:`~ingestion.chunker.TextChunker`.

        Returns:
            Chunks augmented with an ``embedding`` (list[float]) key.

        Raises:
            NotImplementedError: Until embedding generation is implemented.
        """
        raise NotImplementedError("Embedding generation not yet implemented.")

    def embed_query(self, query: str) -> list[float]:
        """
        Generate an embedding for a single query string.

        Args:
            query: Query text to embed.

        Returns:
            Dense vector as a list of floats.

        Raises:
            NotImplementedError: Until embedding generation is implemented.
        """
        raise NotImplementedError("Query embedding not yet implemented.")
