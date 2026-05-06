"""Rule-based fatigue risk scoring (0-100)."""


def score_duty(entry: dict) -> dict:
    """Score a single duty entry for fatigue risk.
    Returns {score, risk_level, violations, breakdown}.
    """
    score = 0
    violations = []
    breakdown = {}

    duty_hrs = float(entry.get("duty_duration_hours", 8))
    rest_hrs = float(entry.get("rest_period_hours", 10))
    num_legs = int(entry.get("num_legs", 1))
    night = int(entry.get("night_duties", 0))
    tz = int(entry.get("time_zones_crossed", 0))
    sleep = float(entry.get("sleep_last_24h", 7))

    # Duty duration penalty: +2 per hour over 8, max +20
    if duty_hrs > 8:
        penalty = min(int((duty_hrs - 8) * 2), 20)
        score += penalty
        breakdown["duty_duration"] = penalty
        if duty_hrs > 12:
            violations.append(f"Extended duty: {duty_hrs:.1f}h exceeds 12h threshold")

    # Rest period penalty: +3 per hour under 10, max +30
    if rest_hrs < 10:
        penalty = min(int((10 - rest_hrs) * 3), 30)
        score += penalty
        breakdown["rest_deficit"] = penalty
        if rest_hrs < 8:
            violations.append(f"Insufficient rest: {rest_hrs:.1f}h below 8h minimum")

    # Night duty penalty: +15 if duty overlaps 02:00-06:00
    if night > 0:
        penalty = 15
        score += penalty
        breakdown["night_duty"] = penalty
        violations.append("Night duty overlaps circadian low (02:00-06:00)")

    # Multi-leg penalty: +5 per leg beyond 2, max +15
    if num_legs > 2:
        penalty = min((num_legs - 2) * 5, 15)
        score += penalty
        breakdown["multi_leg"] = penalty

    # Timezone crossing: +5 per tz, max +20
    if tz > 0:
        penalty = min(tz * 5, 20)
        score += penalty
        breakdown["timezone"] = penalty
        if tz >= 4:
            violations.append(f"Significant jet lag risk: {tz} time zones crossed")

    # Sleep deficit: +2 per hour below 7, max +14
    if sleep < 7:
        penalty = min(int((7 - sleep) * 2), 14)
        score += penalty
        breakdown["sleep_deficit"] = penalty

    score = min(score, 100)

    if score <= 30:
        risk_level = "low"
    elif score <= 60:
        risk_level = "moderate"
    else:
        risk_level = "high"

    return {
        "score": score,
        "risk_level": risk_level,
        "violations": violations,
        "breakdown": breakdown,
    }


def score_schedule(entries: list[dict]) -> dict:
    """Score an entire schedule. Returns per-entry scores + aggregate."""
    results = []
    consecutive_early = 0

    for entry in entries:
        result = score_duty(entry)
        result["entry"] = entry
        results.append(result)

        # Track consecutive early starts for cumulative penalty
        duty_start = entry.get("duty_start", "")
        if isinstance(duty_start, str) and "T" in duty_start:
            hour = int(duty_start.split("T")[1][:2])
            if hour < 6:
                consecutive_early += 1
            else:
                consecutive_early = 0

        if consecutive_early > 3:
            result["score"] = min(result["score"] + 10, 100)
            result["violations"].append("Cumulative fatigue: >3 consecutive early starts")

    scores = [r["score"] for r in results]
    avg = sum(scores) / len(scores) if scores else 0
    max_score = max(scores) if scores else 0

    if max_score > 60:
        overall_risk = "high"
    elif avg > 30:
        overall_risk = "moderate"
    else:
        overall_risk = "low"

    return {
        "entries": results,
        "average_score": round(avg, 1),
        "max_score": max_score,
        "overall_risk": overall_risk,
        "total_entries": len(results),
    }
