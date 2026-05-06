"""Cross-module chain: Fatigue Assessment (C) → SOP/Regulation Lookup (A)."""

import logging
from modules.module_a.retriever import SOPRetriever
from modules.module_a.reranker import rerank
from modules.module_a.generator import generate_answer

logger = logging.getLogger(__name__)

FATIGUE_QUERIES = [
    "FAA rest requirements for flight crew duty time limitations",
    "FAR Part 117 flight duty period limits",
    "augmented crew requirements for extended operations",
    "fatigue risk management system FRMS requirements",
]


def enrich_with_regulations(assessment: dict, db_client=None) -> dict:
    """If fatigue risk is high, auto-query Module A for relevant regulations."""
    if assessment.get("overall_risk") != "high" and assessment.get("max_score", 0) <= 60:
        assessment["regulation_enrichment"] = []
        return assessment

    retriever = SOPRetriever(db_client)
    reg_results = []

    for query in FATIGUE_QUERIES:
        try:
            chunks = retriever.retrieve(query, top_k=10)
            if chunks:
                ranked = rerank(query, chunks, top_k=2)
                if ranked:
                    result = generate_answer(query, ranked)
                    reg_results.append({
                        "query": query,
                        "answer": result["answer"],
                        "citations": result["citations"],
                    })
        except Exception as e:
            logger.warning(f"Regulation lookup failed for '{query}': {e}")

    assessment["regulation_enrichment"] = reg_results
    return assessment
