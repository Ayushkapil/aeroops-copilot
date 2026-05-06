"""RQ1: RAG Pipeline Evaluation — citation accuracy, answer relevance, precision@5."""

import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from modules.module_a.retriever import SOPRetriever
from modules.module_a.reranker import rerank
from modules.module_a.generator import generate_answer
from db.pgvector_client import PgVectorClient

# Sample Q&A pairs for evaluation
QA_PAIRS = [
    {"question": "What are the stabilized approach criteria?", "expected_source": "stabilized_approach_sop", "expected_keywords": ["1000 feet", "500 feet", "VREF"]},
    {"question": "When must a go-around be executed?", "expected_source": "stabilized_approach_sop", "expected_keywords": ["go-around", "stabilized", "descent rate"]},
    {"question": "What are the IFR fuel reserve requirements?", "expected_source": "fuel_reserves_sop", "expected_keywords": ["45 minutes", "alternate"]},
    {"question": "What is the company policy for IFR fuel reserves?", "expected_source": "fuel_reserves_sop", "expected_keywords": ["60-minute", "company"]},
    {"question": "What are the immediate actions for smoke in the cockpit?", "expected_source": "smoke_fumes_emergency_sop", "expected_keywords": ["oxygen masks", "MAYDAY", "descent"]},
    {"question": "How should electrical smoke be handled?", "expected_source": "smoke_fumes_emergency_sop", "expected_keywords": ["load shedding", "electrical", "galley"]},
    {"question": "What is the VFR fuel reserve for night flights?", "expected_source": "fuel_reserves_sop", "expected_keywords": ["45 minutes", "night"]},
    {"question": "What descent rate requires a mandatory go-around?", "expected_source": "stabilized_approach_sop", "expected_keywords": ["1500", "go-around"]},
]


def evaluate():
    db = PgVectorClient()
    retriever = SOPRetriever(db)

    results = {"total": len(QA_PAIRS), "citation_correct": 0, "answer_relevant": 0, "retrieval_hits": 0}

    for qa in QA_PAIRS:
        q = qa["question"]
        print(f"\n--- Q: {q}")

        chunks = retriever.retrieve(q, top_k=20)
        ranked = rerank(q, chunks, top_k=5)
        answer_data = generate_answer(q, ranked)

        # Citation accuracy: does at least one citation match expected source?
        citations = answer_data.get("citations", [])
        if any(qa["expected_source"] in c.get("source", "") for c in citations):
            results["citation_correct"] += 1
            print("  ✓ Citation correct")
        else:
            print(f"  ✗ Citation miss (got: {[c.get('source') for c in citations]})")

        # Answer relevance: do expected keywords appear in answer?
        answer = answer_data.get("answer", "").lower()
        hits = sum(1 for kw in qa["expected_keywords"] if kw.lower() in answer)
        if hits >= len(qa["expected_keywords"]) // 2:
            results["answer_relevant"] += 1
            print("  ✓ Answer relevant")
        else:
            print(f"  ✗ Answer relevance low ({hits}/{len(qa['expected_keywords'])} keywords)")

        # Retrieval precision@5: does expected source appear in top-5?
        if any(qa["expected_source"] in c.get("metadata", {}).get("source_file", "") for c in ranked):
            results["retrieval_hits"] += 1
            print("  ✓ Retrieval hit")

    print("\n=== RESULTS ===")
    for k, v in results.items():
        if k != "total":
            print(f"  {k}: {v}/{results['total']} ({v/results['total']*100:.0f}%)")


if __name__ == "__main__":
    evaluate()
