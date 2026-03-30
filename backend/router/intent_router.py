"""
Intent Router — LLM-based intent classification.

Classifies incoming user requests and routes them to the appropriate
module (Module A: SOP RAG, Module B: Incident Analysis, Module C:
Fatigue Risk Planner).
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


class IntentRouter:
    """
    LLM-based intent classifier that determines which module(s) to invoke
    based on the user's input type and content.

    Supported intents:
        - ``sop_query``  → Module A
        - ``incident_analysis`` → Module B (chains to Module A)
        - ``fatigue_assessment`` → Module C (chains to Module A if high risk)
    """

    def classify(self, text: str) -> str:
        """
        Classify the intent of a user query.

        Args:
            text: Raw user input text.

        Returns:
            Intent label string.

        Raises:
            NotImplementedError: Until LLM classifier is implemented.
        """
        raise NotImplementedError("LLM intent classification not yet implemented.")

    def route(self, intent: str, payload: dict) -> dict:
        """
        Route the request to the appropriate module handler.

        Args:
            intent: Classified intent label.
            payload: Request payload dict.

        Returns:
            Module response dict.

        Raises:
            NotImplementedError: Until routing logic is implemented.
        """
        raise NotImplementedError("Intent routing not yet implemented.")


@router.post("/query")
async def query(body: dict) -> dict:
    """Route a text query through the intent router (placeholder)."""
    return {"status": "not_implemented", "message": "Intent router coming soon."}
