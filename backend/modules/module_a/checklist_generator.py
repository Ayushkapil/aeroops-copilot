"""Generates structured checklists from retrieved SOP chunks."""

import os
import json
import logging
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

CHECKLIST_PROMPT = """You are an aviation safety expert. Extract a CHECKLIST from the provided SOP context.

RULES:
1. ONLY use information from the provided context. Never invent steps.
2. Each step MUST include a citation: [Source: filename, Section, Page X]
3. If the context doesn't contain a clear procedure, say so.
4. Include any WARNINGS, CAUTIONS, or NOTES in the correct position.
5. Group steps by phase if applicable.

Return ONLY valid JSON in this exact format:
{
  "title": "Procedure title",
  "applicable_conditions": "When this checklist applies",
  "steps": [
    {
      "step_number": 1,
      "action": "What to do",
      "details": "Additional detail if any (or empty string)",
      "callout": "WARNING/CAUTION/NOTE or empty string",
      "source": "filename",
      "section": "Section X.X",
      "page": 1
    }
  ],
  "notes": ["Any general notes about this procedure"]
}"""


class ChecklistStep(BaseModel):
    step_number: int
    action: str
    details: str = ""
    callout: str = ""
    source: str = ""
    section: str = ""
    page: int = 0


class Checklist(BaseModel):
    title: str
    applicable_conditions: str = ""
    steps: list[ChecklistStep] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


def generate_checklist(query: str, chunks: list[dict]) -> dict:
    if not chunks:
        return {
            "title": "No procedure found",
            "steps": [],
            "notes": ["No relevant SOP content was found for this query."],
            "citations": [],
        }

    context_parts = []
    citations = []
    for i, c in enumerate(chunks):
        meta = c.get("metadata", {})
        src = meta.get("source_file", "Unknown")
        sec = meta.get("section_title", "N/A")
        sub = meta.get("subsection", "")
        pg = meta.get("page_number", "N/A")
        label = f"[{i+1}] Source: {src}, Section: {sec}"
        if sub:
            label += f", Subsection: {sub}"
        label += f", Page: {pg}"
        context_parts.append(f"{label}\n{c['content']}")
        citations.append({"source": src, "section": sec, "page": pg})

    context_block = "\n\n---\n\n".join(context_parts)

    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    try:
        response = llm.invoke([
            SystemMessage(content=CHECKLIST_PROMPT),
            HumanMessage(content=f"Context:\n{context_block}\n\nQuery: {query}"),
        ])
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
        data = json.loads(raw)
        checklist = Checklist(**data)
        result = checklist.model_dump()
        result["citations"] = citations
        return result
    except Exception as e:
        logger.error(f"Checklist generation error: {e}")
        return {
            "title": "Checklist generation failed",
            "steps": [],
            "notes": [f"Error: {str(e)}"],
            "citations": citations,
        }
