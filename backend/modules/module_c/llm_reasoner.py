"""LLM contextual reasoning for fatigue risk assessment."""

import os
import json
import logging
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an aviation fatigue risk management expert. Given a fatigue score, risk level, schedule data, and rule violations, provide contextual reasoning and mitigations.

Return ONLY valid JSON with these fields:
{
  "reasoning": "Detailed explanation of why this schedule poses fatigue risk",
  "peak_risk_window": "The time window with highest fatigue risk (e.g., '02:00-06:00 on Day 2')",
  "mitigations": ["list of specific, actionable mitigation recommendations"],
  "augmentation_needed": true/false
}"""


def reason(score: int, category: str, schedule_data: dict, rule_violations: list) -> dict:
    """Generate LLM-based contextual reasoning for fatigue assessment."""
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    context = f"""Fatigue Score: {score}/100
Risk Level: {category}
Schedule Details: {json.dumps(schedule_data, default=str)}
Rule Violations: {json.dumps(rule_violations)}"""

    try:
        response = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=context),
        ])
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
        return json.loads(raw)
    except Exception as e:
        logger.error(f"LLM reasoning error: {e}")
        return {
            "reasoning": f"Schedule scored {score}/100 ({category} risk). Violations: {', '.join(rule_violations) if rule_violations else 'None'}",
            "peak_risk_window": "Unable to determine",
            "mitigations": ["Review schedule with crew scheduling", "Ensure minimum rest requirements are met"],
            "augmentation_needed": score > 60,
        }
