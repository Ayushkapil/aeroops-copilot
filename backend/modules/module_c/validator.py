"""
Module C — Fatigue Risk Planner: Schedule Validator.

Validates an uploaded pilot schedule CSV file for structural correctness
and required columns before processing by the fatigue scorer.
"""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {"duty_start", "duty_end", "rest_period_hours"}


class ScheduleValidator:
    """
    Validates the structure and content of a pilot schedule DataFrame
    loaded from a CSV upload.

    Typical usage:
        validator = ScheduleValidator()
        validator.validate(schedule_df)  # raises ValueError on invalid input
    """

    def validate(self, schedule_df: pd.DataFrame) -> None:
        """
        Validate that the schedule DataFrame contains the required columns
        and has no obviously invalid values.

        Args:
            schedule_df: DataFrame loaded from the uploaded CSV.

        Raises:
            ValueError: If required columns are missing or data is invalid.
            NotImplementedError: Until full validation logic is implemented.
        """
        missing = REQUIRED_COLUMNS - set(schedule_df.columns)
        if missing:
            raise ValueError(f"Schedule CSV is missing required columns: {missing}")
        raise NotImplementedError("Full schedule validation not yet implemented.")
