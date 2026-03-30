"""
Module B — Incident Analysis Engine: Pydantic Output Schemas.

Defines the validated output structure for incident analysis results.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class TimelineEvent(BaseModel):
    """A single event in the incident timeline."""

    time: str = Field(description="Time or relative time of the event (e.g. 'T-5 min')")
    description: str = Field(description="Brief description of the event")


class IncidentAnalysis(BaseModel):
    """
    Structured output schema for an analysed aviation incident report.

    Example::

        {
            "timeline": [{"time": "T-5 min", "description": "ATC clearance issued"}],
            "phase_of_flight": "approach",
            "event_tags": ["runway_incursion", "communication_failure"],
            "contributing_factors": ["fatigue", "inadequate_briefing"],
            "sop_links": ["AIM 4-3-18", "AC 91-73B"]
        }
    """

    timeline: list[TimelineEvent] = Field(
        default_factory=list,
        description="Chronological sequence of events leading to the incident",
    )
    phase_of_flight: str = Field(
        description="Flight phase during which the incident occurred (e.g. 'approach')"
    )
    event_tags: list[str] = Field(
        default_factory=list,
        description="Short keyword tags classifying the incident type",
    )
    contributing_factors: list[str] = Field(
        default_factory=list,
        description="Human, technical, or environmental factors contributing to the incident",
    )
    sop_links: list[str] = Field(
        default_factory=list,
        description="Relevant SOP/regulation references (e.g. 'AIM 4-3-18')",
    )
