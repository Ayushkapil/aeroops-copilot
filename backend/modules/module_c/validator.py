"""CSV schedule validation for fatigue assessment."""

import pandas as pd
import io
from datetime import datetime

REQUIRED_COLUMNS = [
    "duty_start", "duty_end", "rest_period_hours", "num_legs",
    "night_duties", "time_zones_crossed", "sleep_last_24h"
]


def validate_schedule(file_bytes: bytes) -> dict:
    """Validate and clean an uploaded CSV schedule.
    Returns {"valid": True, "data": list[dict], "rows": int} or {"valid": False, "errors": [...]}.
    """
    errors = []
    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
    except Exception as e:
        return {"valid": False, "errors": [f"Could not parse CSV: {e}"], "data": [], "rows": 0}

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        errors.append(f"Missing columns: {', '.join(missing)}")
        return {"valid": False, "errors": errors, "data": [], "rows": 0}

    # Parse dates
    for col in ["duty_start", "duty_end"]:
        try:
            df[col] = pd.to_datetime(df[col])
        except Exception:
            errors.append(f"Could not parse dates in column '{col}'")

    # Validate numeric columns
    for col in ["rest_period_hours", "num_legs", "night_duties", "time_zones_crossed", "sleep_last_24h"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if errors:
        return {"valid": False, "errors": errors, "data": [], "rows": 0}

    # Compute duty_duration_hours
    df["duty_duration_hours"] = (df["duty_end"] - df["duty_start"]).dt.total_seconds() / 3600

    records = df.to_dict(orient="records")
    # Convert timestamps to strings for JSON
    for r in records:
        for k, v in r.items():
            if isinstance(v, (pd.Timestamp, datetime)):
                r[k] = v.isoformat()

    return {"valid": True, "data": records, "rows": len(records), "errors": []}
