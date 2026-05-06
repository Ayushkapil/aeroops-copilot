"""RQ3: Fatigue Scoring Evaluation — uses known high-risk schedules as ground truth."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from modules.module_c.scorer import score_schedule

# Ground truth: schedules with known risk levels based on NASA ASRS fatigue-tagged patterns
GROUND_TRUTH = [
    # Known HIGH risk: red-eye, short rest, many legs, timezone crossing
    {"entry": {"duty_duration_hours": 12, "rest_period_hours": 6, "num_legs": 3, "night_duties": 1, "time_zones_crossed": 4, "sleep_last_24h": 4.5}, "expected": "high"},
    {"entry": {"duty_duration_hours": 16, "rest_period_hours": 7, "num_legs": 4, "night_duties": 1, "time_zones_crossed": 3, "sleep_last_24h": 5}, "expected": "high"},
    {"entry": {"duty_duration_hours": 14, "rest_period_hours": 5, "num_legs": 2, "night_duties": 1, "time_zones_crossed": 2, "sleep_last_24h": 4}, "expected": "high"},
    # Known MODERATE risk
    {"entry": {"duty_duration_hours": 10, "rest_period_hours": 9, "num_legs": 3, "night_duties": 0, "time_zones_crossed": 1, "sleep_last_24h": 6}, "expected": "moderate"},
    {"entry": {"duty_duration_hours": 9, "rest_period_hours": 8, "num_legs": 2, "night_duties": 1, "time_zones_crossed": 0, "sleep_last_24h": 6.5}, "expected": "moderate"},
    # Known LOW risk
    {"entry": {"duty_duration_hours": 8, "rest_period_hours": 12, "num_legs": 2, "night_duties": 0, "time_zones_crossed": 0, "sleep_last_24h": 7.5}, "expected": "low"},
    {"entry": {"duty_duration_hours": 7, "rest_period_hours": 14, "num_legs": 1, "night_duties": 0, "time_zones_crossed": 0, "sleep_last_24h": 8}, "expected": "low"},
    {"entry": {"duty_duration_hours": 6, "rest_period_hours": 11, "num_legs": 2, "night_duties": 0, "time_zones_crossed": 0, "sleep_last_24h": 7}, "expected": "low"},
]


def evaluate():
    correct = 0
    high_correct = 0
    high_total = 0
    false_positives = 0

    for gt in GROUND_TRUTH:
        result = score_schedule([gt["entry"]])
        predicted = result["overall_risk"]
        expected = gt["expected"]

        match = predicted == expected
        if match:
            correct += 1
        if expected == "high":
            high_total += 1
            if predicted == "high":
                high_correct += 1
        if predicted == "high" and expected != "high":
            false_positives += 1

        symbol = "✓" if match else "✗"
        print(f"  {symbol} Score: {result['max_score']:3d} | Predicted: {predicted:8s} | Expected: {expected:8s}")

    n = len(GROUND_TRUTH)
    print(f"\n=== RESULTS ===")
    print(f"  Overall accuracy: {correct}/{n} ({correct/n*100:.0f}%)")
    print(f"  High-risk detection: {high_correct}/{high_total} ({high_correct/high_total*100:.0f}%)" if high_total else "  No high-risk cases")
    print(f"  False positive rate: {false_positives}/{n - high_total}" if (n - high_total) else "")


if __name__ == "__main__":
    evaluate()
