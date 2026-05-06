"""Pydantic schemas for incident analysis output."""

from pydantic import BaseModel, Field


class TimelineEvent(BaseModel):
    timestamp: str = Field(description="Time or phase of the event")
    event: str = Field(description="Description of what happened")


class IncidentAnalysis(BaseModel):
    summary: str = Field(description="Brief summary of the incident")
    phase_of_flight: str = Field(description="e.g., cruise, approach, takeoff, taxi")
    event_tags: list[str] = Field(description="e.g., runway_incursion, communication_failure")
    timeline: list[TimelineEvent] = Field(description="Chronological event sequence")
    contributing_factors: list[str] = Field(description="Root causes and contributing factors")
    severity: str = Field(description="minor, moderate, or serious")
    sop_links: list[str] = Field(description="Relevant SOP/regulation references e.g. AIM 4-3-18")
    recommendations: list[str] = Field(description="Safety recommendations")
