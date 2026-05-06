"""RQ2: Incident Extraction Evaluation — timeline accuracy, tag F1, schema completeness."""

import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from modules.module_b.analyzer import analyze_incident
from modules.module_b.schema import IncidentAnalysis

SAMPLE_INCIDENTS = [
    {
        "narrative": open(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'asrs', 'asrs_report_001.txt')).read() if os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'asrs', 'asrs_report_001.txt')) else "During approach at SFO, FO called not stabilized at 800ft AGL. Airspeed was VREF+25. Go-around executed. Second approach was normal.",
        "expected_phase": "approach",
        "expected_tags": ["unstabilized_approach", "go_around", "speed_deviation"],
        "expected_severity": "moderate",
    },
    {
        "narrative": open(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'asrs', 'asrs_report_002.txt')).read() if os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'asrs', 'asrs_report_002.txt')) else "While taxiing at ATL, cleared to cross runway 27L. Regional jet on short final 1 mile out. Stopped on runway. Tower issued go-around to arriving aircraft. Runway incursion category B.",
        "expected_phase": "taxi",
        "expected_tags": ["runway_incursion", "communication_failure", "atc_error"],
        "expected_severity": "serious",
    },
]


def evaluate():
    results = {"total": len(SAMPLE_INCIDENTS), "schema_valid": 0, "phase_correct": 0, "tag_f1_sum": 0, "has_timeline": 0}

    for sample in SAMPLE_INCIDENTS:
        print(f"\n--- Analyzing incident...")
        analysis = analyze_incident(sample["narrative"])

        # Schema completeness
        try:
            IncidentAnalysis(**analysis)
            results["schema_valid"] += 1
            print("  ✓ Schema valid")
        except Exception as e:
            print(f"  ✗ Schema invalid: {e}")

        # Phase accuracy
        if analysis.get("phase_of_flight", "").lower().replace(" ", "_") == sample["expected_phase"]:
            results["phase_correct"] += 1
            print(f"  ✓ Phase correct: {analysis['phase_of_flight']}")
        else:
            print(f"  ✗ Phase: got '{analysis.get('phase_of_flight')}', expected '{sample['expected_phase']}'")

        # Tag F1
        predicted = set(t.lower().replace(" ", "_") for t in analysis.get("event_tags", []))
        expected = set(t.lower() for t in sample["expected_tags"])
        if predicted and expected:
            tp = len(predicted & expected)
            precision = tp / len(predicted) if predicted else 0
            recall = tp / len(expected) if expected else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            results["tag_f1_sum"] += f1
            print(f"  Tag F1: {f1:.2f} (predicted: {predicted}, expected: {expected})")

        # Timeline presence
        if len(analysis.get("timeline", [])) >= 2:
            results["has_timeline"] += 1
            print(f"  ✓ Timeline: {len(analysis['timeline'])} events")

    n = results["total"]
    print("\n=== RESULTS ===")
    print(f"  Schema valid: {results['schema_valid']}/{n}")
    print(f"  Phase correct: {results['phase_correct']}/{n}")
    print(f"  Avg tag F1: {results['tag_f1_sum']/n:.2f}")
    print(f"  Has timeline: {results['has_timeline']}/{n}")


if __name__ == "__main__":
    evaluate()
