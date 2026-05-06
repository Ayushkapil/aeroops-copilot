"""SOP RAG retriever with checklist-aware search."""

from ingestion.embedder import embed_query
from db.pgvector_client import PgVectorClient


class SOPRetriever:
    def __init__(self, db_client: PgVectorClient = None):
        self.db = db_client or PgVectorClient()

    def retrieve(self, query: str, top_k: int = 20) -> list[dict]:
        """Embed query and run cosine similarity search."""
        query_embedding = embed_query(query)
        results = self.db.similarity_search(query_embedding, top_k=top_k)
        return results

    def retrieve_checklist(self, query: str, top_k: int = 30) -> list[dict]:
        """Retrieve with preference for checklist-containing chunks."""
        query_embedding = embed_query(query)
        results = self.db.similarity_search(query_embedding, top_k=top_k)

        for r in results:
            meta = r.get("metadata", {})
            if meta.get("is_checklist"):
                r["similarity"] = r.get("similarity", 0) + 0.1

        results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        return results

    def retrieve_by_section(self, query: str, top_k: int = 20) -> list[dict]:
        """Retrieve, then pull adjacent chunks from the same section."""
        results = self.retrieve(query, top_k=top_k)
        if not results:
            return results

        best = results[0]
        best_section = best.get("metadata", {}).get("section_title", "")
        best_source = best.get("metadata", {}).get("source_file", "")

        section_chunks = [
            r for r in results
            if r.get("metadata", {}).get("section_title") == best_section
            and r.get("metadata", {}).get("source_file") == best_source
        ]
        section_chunks.sort(key=lambda x: x.get("metadata", {}).get("chunk_index", 0))

        other_chunks = [r for r in results if r not in section_chunks]
        return section_chunks + other_chunks[:5]
