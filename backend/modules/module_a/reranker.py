"""Cross-encoder reranking for retrieved chunks."""

import math
import logging
from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

_model = None


def get_model():
    global _model
    if _model is None:
        logger.info("Loading cross-encoder model...")
        _model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _model


def _sigmoid(x: float) -> float:
    """Map unbounded logit to (0, 1) probability."""
    # Clamp to avoid math overflow
    if x < -50:
        return 0.0
    if x > 50:
        return 1.0
    return 1.0 / (1.0 + math.exp(-x))


def rerank(query: str, chunks: list[dict], top_k: int = 5) -> list[dict]:
    """Rerank chunks using cross-encoder, returning top_k with normalized scores."""
    if not chunks:
        return []

    model = get_model()
    pairs = [(query, c["content"]) for c in chunks]
    raw_scores = model.predict(pairs)

    for chunk, raw in zip(chunks, raw_scores):
        raw_f = float(raw)
        chunk["rerank_logit"] = raw_f       # keep original for debugging
        chunk["rerank_score"] = _sigmoid(raw_f)  # normalized [0, 1]

    ranked = sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)
    return ranked[:top_k]
