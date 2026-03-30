"""
Evaluation: RQ2 — Incident Extraction Evaluation (Module B).

Research Question 2: How accurately does Module B extract structured
incident data compared to a human-labelled ASRS baseline?

Metrics:
    - Tag Accuracy (event_tags match rate)
    - Timeline F1 (event detection F1-score)
    - Contributing Factor Accuracy

Ground truth: Human-labelled ASRS incident structure.
"""

from __future__ import annotations


def load_labelled_incidents(path: str) -> list[dict]:
    """
    Load human-labelled ASRS incident annotations.

    Args:
        path: Path to the annotations file (JSON/CSV).

    Returns:
        List of labelled incident dicts.

    Raises:
        NotImplementedError: Until data loading is implemented.
    """
    raise NotImplementedError("Labelled incident loading not yet implemented.")


def evaluate_incident_extraction(
    labelled: list[dict], analyzer: object
) -> dict:
    """
    Compare Module B extraction output against human labels.

    Args:
        labelled: Human-labelled incident annotations.
        analyzer: Initialised Module B IncidentAnalyzer instance.

    Returns:
        Dict with ``tag_accuracy`` (float) and ``timeline_f1`` (float).

    Raises:
        NotImplementedError: Until evaluation logic is implemented.
    """
    raise NotImplementedError("Incident extraction evaluation not yet implemented.")


def compute_tag_accuracy(predicted: list[str], expected: list[str]) -> float:
    """
    Compute exact-match accuracy for event tags.

    Args:
        predicted: Predicted event tag list.
        expected: Ground-truth tag list.

    Returns:
        Accuracy as a float between 0 and 1.

    Raises:
        NotImplementedError: Until tag accuracy computation is implemented.
    """
    raise NotImplementedError("Tag accuracy computation not yet implemented.")


if __name__ == "__main__":
    print("RQ2 Incident extraction evaluation — not yet implemented.")
