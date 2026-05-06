"""Cross-module chain: Incident Analysis (B) → SOP Lookup (A)."""

import logging
from modules.module_a.retriever import SOPRetriever
from modules.module_a.reranker import rerank
from modules.module_a.generator import generate_answer

logger = logging.getLogger(__name__)


def enrich_with_sop(analysis: dict, db_client=None) -> dict:
    """After Module B produces an IncidentAnalysis, look up relevant SOPs."""
    retriever = SOPRetriever(db_client)
    sop_results = []

    # Query for each SOP link and event tag
    search_terms = analysis.get("sop_links", []) + analysis.get("event_tags", [])[:3]

    for term in search_terms[:5]:  # Limit to 5 queries
        query = f"aviation procedure: {term}"
        try:
            chunks = retriever.retrieve(query, top_k=10)
            if chunks:
                ranked = rerank(query, chunks, top_k=2)
                if ranked:
                    result = generate_answer(query, ranked)
                    sop_results.append({
                        "query": term,
                        "answer": result["answer"],
                        "citations": result["citations"],
                    })
        except Exception as e:
            logger.warning(f"SOP lookup failed for '{term}': {e}")

    analysis["sop_enrichment"] = sop_results
    return analysis
