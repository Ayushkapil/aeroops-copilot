"""Large document incident analysis using chunk-and-summarize."""

import os
import json
import logging
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
from .schema import IncidentAnalysis

load_dotenv()
logger = logging.getLogger(__name__)

CHUNK_LIMIT = 12000

SUMMARIZE_PROMPT = """You are an aviation safety analyst. Read this section of an incident report and extract key facts.
Return ONLY valid JSON:
{
  "events": ["list of events that happened in this section"],
  "factors": ["contributing factors mentioned"],
  "phase": "flight phase if mentioned, else null",
  "severity_indicators": ["any severity indicators"],
  "procedures_mentioned": ["any SOP/regulation references"]
}"""

MERGE_PROMPT = """You are an aviation safety analyst. You have summaries from multiple sections of an incident report.
Merge them into a single structured analysis.

Return ONLY valid JSON with these exact keys:
{
  "summary": "Brief summary of the entire incident",
  "phase_of_flight": "one of: preflight, taxi, takeoff, climb, cruise, descent, approach, landing, go_around",
  "event_tags": ["list of relevant tags"],
  "timeline": [{"timestamp": "phase or time", "event": "what happened"}],
  "contributing_factors": ["factor1", "factor2"],
  "severity": "minor or moderate or serious",
  "sop_links": ["relevant SOP references"],
  "recommendations": ["recommendation1", "recommendation2"]
}"""


def get_llm():
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        model_kwargs={"response_format": {"type": "json_object"}},
    )


def split_text(text: str, limit: int = CHUNK_LIMIT) -> list[str]:
    if len(text) <= limit:
        return [text]
    sections = []
    start = 0
    while start < len(text):
        end = min(start + limit, len(text))
        if end < len(text):
            nl = text.rfind("\n\n", start + limit // 2, end)
            if nl > start:
                end = nl
        sections.append(text[start:end].strip())
        start = end
    return sections


def summarize_section(llm, section_text: str) -> dict:
    try:
        response = llm.invoke([
            SystemMessage(content=SUMMARIZE_PROMPT),
            HumanMessage(content=section_text),
        ])
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
        return json.loads(raw)
    except Exception as e:
        logger.warning(f"Section summarize failed: {e}")
        return {"events": [], "factors": [], "phase": None,
                "severity_indicators": [], "procedures_mentioned": []}


def analyze_large_incident(narrative: str) -> dict:
    """Analyze a large incident report using chunk-and-merge strategy."""
    llm = get_llm()

    sections = split_text(narrative)
    logger.info(f"Split document into {len(sections)} sections")

    section_summaries = []
    for i, section in enumerate(sections):
        logger.info(f"Summarizing section {i+1}/{len(sections)}")
        summary = summarize_section(llm, section)
        section_summaries.append(summary)

    merged_input = json.dumps(section_summaries, indent=2)

    if len(merged_input) > CHUNK_LIMIT:
        condensed = []
        for s in section_summaries:
            c = {k: v for k, v in s.items() if v}
            if c:
                condensed.append(c)
        merged_input = json.dumps(condensed, indent=2)

    try:
        response = llm.invoke([
            SystemMessage(content=MERGE_PROMPT),
            HumanMessage(content=f"Section summaries:\n{merged_input}"),
        ])
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
        data = json.loads(raw)
        analysis = IncidentAnalysis(**data)
        return analysis.model_dump()
    except Exception as e:
        logger.error(f"Merge analysis failed: {e}")
        return IncidentAnalysis(
            summary="Analysis of large document partially completed.",
            phase_of_flight="unknown",
            event_tags=["large_document"],
            timeline=[],
            contributing_factors=["Document too large for single-pass analysis"],
            severity="moderate",
            sop_links=[],
            recommendations=["Manual review recommended for full-length reports"],
        ).model_dump()
