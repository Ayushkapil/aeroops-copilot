"""LLM answer generation with structured, cited output for SOP queries."""

import os
import json
import logging
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
from utils.tokens import trim_context_to_limit

load_dotenv()
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an aviation safety expert assistant. Answer ONLY using the provided context.
If the answer is not in the context, say 'I could not find this information in the available SOPs.'

You MUST return ONLY valid JSON in this exact format:
{
  "summary": "1-2 sentence summary of the answer",
  "type": "checklist OR explanation",
  "points": [
    {
      "text": "The main point or action step",
      "detail": "Additional detail if needed, or empty string",
      "callout": "WARNING or CAUTION or NOTE or empty string",
      "source_file": "filename.txt",
      "section": "Section X.X",
      "page": 1
    }
  ],
  "additional_notes": ["Any extra context worth mentioning"]
}

Rules:
- Use type "checklist" if the answer involves steps, procedures, or sequential actions
- Use type "explanation" if the answer is factual/informational
- Keep each point concise — max 1-2 sentences
- Every point MUST have source_file, section, and page from the context provided
- Include WARNING/CAUTION/NOTE callouts where they appear in the source
- Do NOT invent information. Only use what is in the context."""


def _compute_confidence(chunks: list[dict]) -> float:
    """Compute confidence from reranker scores.
    
    Uses weighted average where top chunks contribute more.
    Returns 0-1 value.
    """
    if not chunks:
        return 0.0
    
    # Weight: top chunk counts 3x, next 2x, rest 1x
    weights = []
    scores = []
    for i, c in enumerate(chunks):
        score = c.get("rerank_score")
        if score is None:
            continue
        weights.append(3.0 if i == 0 else (2.0 if i == 1 else 1.0))
        scores.append(score)
    
    if not scores:
        return 0.0
    
    weighted_sum = sum(w * s for w, s in zip(weights, scores))
    total_weight = sum(weights)
    return weighted_sum / total_weight


def generate_answer(query: str, chunks: list[dict]) -> dict:
    """Generate a structured, cited answer from retrieved chunks."""
    if not chunks:
        return {
            "answer": None,
            "structured": {
                "summary": "I could not find this information in the available SOPs.",
                "type": "explanation",
                "points": [],
                "additional_notes": [],
            },
            "citations": [],
            "confidence": 0.0,
        }

    # IMPORTANT: compute confidence BEFORE trimming so we use all reranked scores
    confidence = _compute_confidence(chunks)
    logger.info(f"Confidence calculated: {confidence:.3f} from {len(chunks)} chunks")

    chunks = trim_context_to_limit(chunks, max_tokens=6000)

    context_parts = []
    citations = []
    for i, c in enumerate(chunks):
        meta = c.get("metadata", {})
        src = meta.get("source_file", "Unknown")
        sec = meta.get("section_title", "N/A")
        pg = meta.get("page_number", "N/A")
        context_parts.append(f"[{i+1}] Source: {src}, Section: {sec}, Page: {pg}\n{c['content']}")
        citations.append({"source": src, "section": sec, "page": pg})

    context_block = "\n\n---\n\n".join(context_parts)

    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "llama-3.1-8b-instant"),
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Context:\n{context_block}\n\nQuestion: {query}"),
    ]

    try:
        response = llm.invoke(messages)
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]

        structured = json.loads(raw)

        plain_parts = [structured.get("summary", "")]
        for p in structured.get("points", []):
            plain_parts.append(f"• {p.get('text', '')}")
        answer = "\n".join(plain_parts)

        return {
            "answer": answer,
            "structured": structured,
            "citations": citations,
            "confidence": round(confidence, 3),
        }
    except Exception as e:
        logger.error(f"LLM generation error: {e}")
        return {
            "answer": "An error occurred while generating the answer. Please try again.",
            "structured": None,
            "citations": citations,
            "confidence": round(confidence, 3),
        }
