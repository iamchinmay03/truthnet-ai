from __future__ import annotations


def compute_risk(text_model: float, evidence_score: float, propagation_score: float,
                graph_score: float, multimodal_score: float, coordination_score: float,
                source_reliability: float, weights: dict[str, float] | None = None) -> dict[str, float | int | str]:
    weights = weights or {
        "text_model": 0.20,
        "evidence_score": 0.30,
        "propagation_score": 0.15,
        "graph_score": 0.15,
        "multimodal_score": 0.10,
        "coordination_score": 0.05,
        "source_reliability": 0.05,
    }

    combined = (
        text_model * weights["text_model"]
        + evidence_score * weights["evidence_score"]
        + propagation_score * weights["propagation_score"]
        + graph_score * weights["graph_score"]
        + multimodal_score * weights["multimodal_score"]
        + coordination_score * weights["coordination_score"]
        + source_reliability * weights["source_reliability"]
    )

    risk_score = int(round((combined * 100)))
    credibility = 100 - risk_score

    if risk_score <= 20:
        level = "Very Low Risk"
    elif risk_score <= 40:
        level = "Low Risk"
    elif risk_score <= 60:
        level = "Moderate Risk"
    elif risk_score <= 80:
        level = "High Risk"
    else:
        level = "Critical Risk"

    return {
        "risk_score": max(0, min(100, risk_score)),
        "credibility": max(0, min(100, credibility)),
        "risk_level": level,
    }
