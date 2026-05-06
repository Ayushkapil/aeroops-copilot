"""LLM-based incident analysis with structured JSON output."""

import os
import json
import logging
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
from .schema import IncidentAnalysis

load_dotenv()
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an aviation safety analyst. Analyze the incident narrative and produce a JSON object with exactly these fields:
{
  "summary": "Brief summary of the incident",
  "phase_of_flight": "one of: preflight, taxi, takeoff, climb, cruise, descent, approach, landing, go_around",
  "event_tags": ["list", "of", "relevant", "tags"],
  "timeline": [{"timestamp": "T+0:00 or phase description", "event": "what happened"}],
  "contributing_factors": ["factor1", "factor2"],
  "severity": "minor or moderate or serious",
  "sop_links": ["relevant SOP/regulation references like AIM 4-3-18, FAR 91.175"],
  "recommendations": ["recommendation1", "recommendation2"]
}
Return ONLY valid JSON. No markdown, no explanation, no preamble."""

STRICT_PROMPT = """You MUST return ONLY a valid JSON object. No text before or after.
The JSON must have these exact keys: summary, phase_of_flight, event_tags, timeline, contributing_factors, severity, sop_links, recommendations.
timeline items must have: timestamp, event.
severity must be one of: minor, moderate, serious."""


def analyze_incident(narrative: str, max_retries: int = 3) -> dict:
    """Analyze an incident narrative and return structured IncidentAnalysis."""
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    last_error = None
    for attempt in range(max_retries):
        prompt = SYSTEM_PROMPT if attempt == 0 else f"{SYSTEM_PROMPT}\n\n{STRICT_PROMPT}"
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"Incident Narrative:\n{narrative}"),
        ]
        try:
            response = llm.invoke(messages)
            raw = response.content.strip()
            # Strip markdown fences if present
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
                if raw.endswith("```"):
                    raw = raw[:-3]
            data = json.loads(raw)
            analysis = IncidentAnalysis(**data)
            return analysis.model_dump()
        except Exception as e:
            last_error = e
            logger.warning(f"Attempt {attempt+1} failed: {e}")

    logger.error(f"All {max_retries} attempts failed: {last_error}")
    # Return minimal valid structure
    return IncidentAnalysis(
        summary="Analysis failed - could not parse incident narrative.",
        phase_of_flight="unknown",
        event_tags=["parse_error"],
        timeline=[],
        contributing_factors=["Automated analysis was unable to process this narrative"],
        severity="moderate",
        sop_links=[],
        recommendations=["Manual review recommended"],
    ).model_dump()
