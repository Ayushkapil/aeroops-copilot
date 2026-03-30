"""
Evaluation: RQ1 — RAG Pipeline Evaluation (Module A).

Research Question 1: Does cross-encoder reranking improve SOP retrieval
quality compared to base vector similarity search?

Metrics:
    - Citation Accuracy (were cited SOPs relevant?)
    - MRR@5 (Mean Reciprocal Rank at 5)

Ground truth: Expert-curated Q&A pairs from FAA documents.
"""

from __future__ import annotations


def load_ground_truth(path: str) -> list[dict]:
    """
    Load ground-truth Q&A pairs for RAG evaluation.

    Args:
        path: Path to the ground-truth JSON/CSV file.

    Returns:
        List of dicts with ``question`` and ``expected_sources`` keys.

    Raises:
        NotImplementedError: Until evaluation data loading is implemented.
    """
    raise NotImplementedError("Ground-truth loading not yet implemented.")


def evaluate_rag_pipeline(ground_truth: list[dict], pipeline: object) -> dict:
    """
    Evaluate the RAG pipeline against ground-truth Q&A pairs.

    Args:
        ground_truth: List of ground-truth evaluation pairs.
        pipeline: Initialised Module A RAG pipeline object.

    Returns:
        Dict with ``citation_accuracy`` (float) and ``mrr_at_5`` (float).

    Raises:
        NotImplementedError: Until evaluation logic is implemented.
    """
    raise NotImplementedError("RAG evaluation not yet implemented.")


def compute_mrr(ranked_lists: list[list[str]], relevant: list[str]) -> float:
    """
    Compute Mean Reciprocal Rank at 5.

    Args:
        ranked_lists: List of ranked source lists (one per query).
        relevant: List of relevant source identifiers.

    Returns:
        MRR@5 score as a float.

    Raises:
        NotImplementedError: Until MRR computation is implemented.
    """
    raise NotImplementedError("MRR computation not yet implemented.")


if __name__ == "__main__":
    print("RQ1 RAG evaluation — not yet implemented.")
