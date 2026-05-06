"""LLM-based intent classification router."""

import os
import logging
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

CLASSIFY_PROMPT = """Classify the user's aviation query into exactly one category:
- "sop_query" — asking about procedures, regulations, standards, policies
- "incident_analysis" — submitting or discussing an incident report
- "fatigue_assessment" — submitting or discussing a schedule/fatigue/duty time
- "general" — general aviation question (will be routed to SOP search)

Examples:
"What are the stabilized approach criteria?" → sop_query
"Analyze this incident report" → incident_analysis  
"Check this crew schedule for fatigue risk" → fatigue_assessment
"What is a TCAS resolution advisory?" → general

Reply with ONLY the category name, nothing else."""


def classify_intent(query: str, has_pdf: bool = False, has_csv: bool = False) -> str:
    """Classify user intent. File type overrides LLM classification."""
    if has_pdf:
        return "incident_analysis"
    if has_csv:
        return "fatigue_assessment"

    try:
        llm = ChatOpenAI(
            model=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
        )
        response = llm.invoke([
            SystemMessage(content=CLASSIFY_PROMPT),
            HumanMessage(content=query),
        ])
        intent = response.content.strip().lower().replace('"', '').replace("'", "")
        valid = {"sop_query", "incident_analysis", "fatigue_assessment", "general"}
        return intent if intent in valid else "general"
    except Exception as e:
        logger.error(f"Intent classification error: {e}")
        return "general"


def route_query(query: str, db_client=None) -> dict:
    """Route a text query through the appropriate module pipeline."""
    from modules.module_a.retriever import SOPRetriever
    from modules.module_a.reranker import rerank
    from modules.module_a.generator import generate_answer

    intent = classify_intent(query)

    # Both sop_query and general route to Module A
    retriever = SOPRetriever(db_client)
    chunks = retriever.retrieve(query, top_k=20)
    ranked = rerank(query, chunks, top_k=5)
    result = generate_answer(query, ranked)

    return {
        "intent": intent,
        "module": "A",
        "response": result,
        "chained_results": None,
        "sources": result.get("citations", []),
    }
