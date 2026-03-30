"""
Evaluation: RQ3 — Fatigue Scoring Evaluation (Module C).

Research Question 3: How accurately does Module C classify fatigue risk
compared to NASA ASRS fatigue-tagged incident labels?

Metrics:
    - Precision, Recall, F1-score (per risk class)
    - Overall accuracy

Ground truth: NASA ASRS fatigue-tagged incidents (avoids circular evaluation).
"""

from __future__ import annotations


def load_fatigue_cases(path: str) -> list[dict]:
    """
    Load NASA ASRS fatigue-tagged incident cases for evaluation.

    Args:
        path: Path to the processed fatigue cases file (JSON/CSV).

    Returns:
        List of case dicts with ``schedule`` and ``label`` keys.

    Raises:
        NotImplementedError: Until data loading is implemented.
    """
    raise NotImplementedError("Fatigue case loading not yet implemented.")


def evaluate_fatigue_scorer(cases: list[dict], scorer: object) -> dict:
    """
    Evaluate the fatigue scorer against ASRS fatigue-tagged ground truth.

    Args:
        cases: List of evaluation cases with ground-truth labels.
        scorer: Initialised Module C FatigueScorer instance.

    Returns:
        Dict with ``precision`` (float), ``recall`` (float), and
        ``f1`` (float) per risk category.

    Raises:
        NotImplementedError: Until evaluation logic is implemented.
    """
    raise NotImplementedError("Fatigue scoring evaluation not yet implemented.")


def compute_classification_metrics(
    y_true: list[str], y_pred: list[str]
) -> dict:
    """
    Compute precision, recall, and F1 for multi-class classification.

    Args:
        y_true: Ground-truth risk category labels.
        y_pred: Predicted risk category labels.

    Returns:
        Dict with per-class and macro-average metrics.

    Raises:
        NotImplementedError: Until metric computation is implemented.
    """
    raise NotImplementedError("Classification metric computation not yet implemented.")


if __name__ == "__main__":
    print("RQ3 Fatigue scoring evaluation — not yet implemented.")
