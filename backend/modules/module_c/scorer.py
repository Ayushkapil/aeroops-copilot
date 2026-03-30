"""
Module C — Fatigue Risk Planner: Rule-Based Scorer.

Computes a numeric fatigue score (0–100) for a pilot schedule using
rule-based heuristics derived from FAA AC 117-1 and FRMS guidelines.

Risk levels:
    - 🟢 Low (0–30)
    - 🟡 Moderate (31–60)
    - 🔴 High (61–100)
"""

from __future__ import annotations

import pandas as pd


class FatigueScorer:
    """
    Rule-based fatigue scorer that analyses a pilot duty schedule and
    returns a numeric risk score with a risk category label.

    Typical usage:
        scorer = FatigueScorer()
        result = scorer.score(schedule_df)
    """

    LOW_THRESHOLD = 30
    HIGH_THRESHOLD = 60

    def score(self, schedule_df: pd.DataFrame) -> dict:
        """
        Calculate a fatigue risk score from a pilot duty schedule.

        Args:
            schedule_df: DataFrame with pilot schedule data (columns such as
                ``duty_start``, ``duty_end``, ``rest_period_hours``,
                ``night_duties``).

        Returns:
            Dict with ``score`` (int 0–100), ``category`` (str), and
            ``rule_violations`` (list[str]).

        Raises:
            NotImplementedError: Until rule-based scoring is implemented.
        """
        raise NotImplementedError("Rule-based fatigue scoring not yet implemented.")

    @classmethod
    def categorise(cls, score: int) -> str:
        """
        Map a numeric fatigue score to a risk category label.

        Args:
            score: Integer fatigue score (0–100).

        Returns:
            One of ``"Low"``, ``"Moderate"``, or ``"High"``.
        """
        if score <= cls.LOW_THRESHOLD:
            return "Low"
        if score <= cls.HIGH_THRESHOLD:
            return "Moderate"
        return "High"
