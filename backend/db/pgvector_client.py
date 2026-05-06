"""PostgreSQL + pgvector client for vector storage and similarity search."""

import os
import json
import logging
from typing import Optional

import psycopg2
from psycopg2.extras import execute_values, RealDictCursor
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

CREATE_EXTENSION = "CREATE EXTENSION IF NOT EXISTS vector;"
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS sop_chunks (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding vector(384),
    content_hash TEXT UNIQUE
);
"""
CREATE_INDEX = """
CREATE INDEX IF NOT EXISTS sop_chunks_embedding_idx
ON sop_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
"""


class PgVectorClient:
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv("DATABASE_URL",
            "postgresql://aeroops:aeroops@localhost:5432/aeroops")
        self._conn = None

    @property
    def conn(self):
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(self.database_url)
            self._conn.autocommit = True
        return self._conn

    def init_db(self):
        """Create the pgvector extension and sop_chunks table."""
        with self.conn.cursor() as cur:
            cur.execute(CREATE_EXTENSION)
            cur.execute(CREATE_TABLE)
            # Only create ivfflat index if enough rows exist
            cur.execute("SELECT COUNT(*) FROM sop_chunks;")
            count = cur.fetchone()[0]
            if count >= 100:
                try:
                    cur.execute(CREATE_INDEX)
                except Exception:
                    pass
        logger.info("Database initialized.")

    def insert_chunks(self, chunks: list[dict]):
        """Insert chunks with embeddings into sop_chunks.
        Each chunk: {content, metadata, embedding, content_hash}
        """
        if not chunks:
            return
        with self.conn.cursor() as cur:
            values = []
            for c in chunks:
                emb_str = "[" + ",".join(str(x) for x in c["embedding"]) + "]"
                values.append((
                    c["content"],
                    json.dumps(c.get("metadata", {})),
                    emb_str,
                    c.get("content_hash", ""),
                ))
            execute_values(cur,
                """INSERT INTO sop_chunks (content, metadata, embedding, content_hash)
                   VALUES %s ON CONFLICT (content_hash) DO NOTHING""",
                values,
                template="(%s, %s::jsonb, %s::vector, %s)"
            )
        logger.info(f"Inserted {len(chunks)} chunks.")

    def similarity_search(self, query_embedding: list[float], top_k: int = 20) -> list[dict]:
        """Cosine similarity search returning top_k chunks."""
        emb_str = "[" + ",".join(str(x) for x in query_embedding) + "]"
        sql = """
            SELECT id, content, metadata,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM sop_chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (emb_str, emb_str, top_k))
            rows = cur.fetchall()
        results = []
        for r in rows:
            meta = r["metadata"] if isinstance(r["metadata"], dict) else json.loads(r["metadata"])
            results.append({
                "id": r["id"],
                "content": r["content"],
                "metadata": meta,
                "similarity": float(r["similarity"]),
            })
        return results

    def get_all_sources(self) -> list[str]:
        """Return distinct source filenames."""
        sql = "SELECT DISTINCT metadata->>'source_file' AS src FROM sop_chunks WHERE metadata->>'source_file' IS NOT NULL;"
        with self.conn.cursor() as cur:
            cur.execute(sql)
            return [r[0] for r in cur.fetchall()]

    def chunk_exists(self, content_hash: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("SELECT 1 FROM sop_chunks WHERE content_hash = %s LIMIT 1;", (content_hash,))
            return cur.fetchone() is not None

    def close(self):
        if self._conn and not self._conn.closed:
            self._conn.close()
