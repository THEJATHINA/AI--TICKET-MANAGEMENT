from typing import Dict

def get_class_confidence(predicted_class: str, class_probs: Dict[str, float]) -> float:
    """
    Retrieves the confidence score for the predicted class.
    This is the probability of the predicted class, scaled to a percentage (0.0 to 100.0).
    """
    confidence = class_probs.get(predicted_class, 0.0)
    return round(float(confidence) * 100.0, 2)

def calculate_overall_confidence(severity_conf: float, priority_conf: float) -> float:
    """
    Calculates overall consolidated confidence as a simple average of severity and priority confidence.
    Returns value scaled to a percentage (0.0 to 100.0).
    """
    overall = (severity_conf + priority_conf) / 2.0
    return round(float(overall), 2)
