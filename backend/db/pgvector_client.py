"""
Database: pgvector Client.

Provides an interface for storing and querying document embeddings in
PostgreSQL + pgvector (Supabase).
"""

from __future__ import annotations

from typing import Any


class PGVectorClient:
    """
    Client for vector similarity search operations against a
    PostgreSQL + pgvector database (hosted on Supabase).

    Typical usage:
        client = PGVectorClient.from_env()
        client.upsert(chunks_with_embeddings)
        results = client.similarity_search(query_embedding, top_k=20)
    """

    def __init__(self, url: str = "", key: str = "") -> None:
        """
        Args:
            url: Supabase project URL.
            key: Supabase service role key.
        """
        self.url = url
        self.key = key
        self._client: Any = None

    @classmethod
    def from_env(cls) -> "PGVectorClient":
        """
        Instantiate a client using environment variables
        ``SUPABASE_URL`` and ``SUPABASE_KEY``.

        Returns:
            Configured :class:`PGVectorClient` instance.
        """
        import os

        return cls(
            url=os.getenv("SUPABASE_URL", ""),
            key=os.getenv("SUPABASE_KEY", ""),
        )

    def upsert(self, chunks: list[dict]) -> None:
        """
        Insert or update embedded document chunks in the vector store.

        Args:
            chunks: List of chunk dicts containing ``text``, ``embedding``,
                and ``metadata`` keys.

        Raises:
            NotImplementedError: Until Supabase upsert is implemented.
        """
        raise NotImplementedError("pgvector upsert not yet implemented.")

    def similarity_search(
        self, query_embedding: list[float], top_k: int = 20
    ) -> list[dict]:
        """
        Perform cosine similarity search against stored embeddings.

        Args:
            query_embedding: Query vector.
            top_k: Number of nearest neighbours to return.

        Returns:
            List of matching chunk dicts sorted by descending similarity.

        Raises:
            NotImplementedError: Until pgvector search is implemented.
        """
        raise NotImplementedError("pgvector similarity search not yet implemented.")
