import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.schemas.analysis import ClaimInput, ClaimResult, EvidenceItem, InvestigationResult
from app.services.trained_model import predict_claim

SENSATIONAL_WORDS = {
    "urgent", "shocking", "miracle", "secret", "exposed", "must read", "banned", "scary",
    "breaking", "unbelievable", "revealed", "alert", "viral", "destroyed"
}

SUPPORTING_SOURCES = [
    {
        "title": "Official government statement on the reported claim",
        "publisher": "Ministry of Information",
        "date": "2026-01-12",
        "url": "https://example.gov/official-statement",
        "summary": "Official records do not support the claim.",
    },
    {
        "title": "Independent verification report",
        "publisher": "FactCheck Institute",
        "date": "2026-01-13",
        "url": "https://example.org/factcheck-report",
        "summary": "Multiple sources contradict the reported timing and scope.",
    },
    {
        "title": "Contextual analysis of viral post",
        "publisher": "Research Desk",
        "date": "2026-01-14",
        "url": "https://example.edu/context-analysis",
        "summary": "Evidence suggests the narrative is incomplete or misleading.",
    },
]


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_claims(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    cleaned = [s.strip() for s in sentences if len(s.strip()) > 20]
    if not cleaned:
        cleaned = [text.strip()]
    claims = []
    for idx, sentence in enumerate(cleaned[:4], start=1):
        claims.append(f"Claim {idx}: {sentence}")
    return claims


def score_claim(text: str) -> tuple[str, float, str, float, int]:
    trained_prediction = predict_claim(text)
    if trained_prediction is not None:
        confidence = trained_prediction["confidence"]
        label = trained_prediction["label"]
        verdict = trained_prediction["verdict"]
        reason = (
            f"The LIAR benchmark text model predicts '{label}' based on language patterns in its training data. "
            "Treat this as a screening signal, not independent verification."
        )
        return verdict, confidence, reason, round(1.0 - confidence, 2), trained_prediction["risk_score"]

    lowered = text.lower()
    sensational_hits = sum(1 for word in SENSATIONAL_WORDS if word in lowered)
    caps = sum(1 for ch in text if ch.isupper())
    has_numeric = any(ch.isdigit() for ch in text)
    suspicious = sensational_hits * 10 + min(caps // 5, 25) + (15 if has_numeric else 0)
    if suspicious >= 45:
        verdict = "LIKELY FALSE"
        confidence = 0.89
        reason = "Sensational framing, urgent language, and unsupported numerical claims increase risk."
        risk = 0.82
    elif suspicious >= 28:
        verdict = "MISLEADING"
        confidence = 0.76
        reason = "The narrative contains persuasive framing with limited independent verification."
        risk = 0.64
    else:
        verdict = "UNVERIFIED"
        confidence = 0.62
        reason = "The statement lacks robust evidence, but not enough signals are present for a confident false classification."
        risk = 0.49

    uncertainty = round(max(0.05, 1.0 - confidence), 2)
    return verdict, confidence, reason, uncertainty, round(risk * 100)


def build_evidence_items(claim: str) -> list[EvidenceItem]:
    items = []
    for idx, item in enumerate(SUPPORTING_SOURCES, start=1):
        evidence = EvidenceItem(
            title=item["title"],
            publisher=item["publisher"],
            date=item["date"],
            url=item["url"],
            relevance=round(0.78 + idx * 0.04, 2),
            direction="contradicting" if idx == 1 else "contextual",
            summary=item["summary"],
        )
        items.append(evidence)
    return items


def build_graph_payload() -> dict[str, Any]:
    return {
        "nodes": [
            {"id": "u1", "label": "@viralwatch", "group": "user", "risk": 89, "size": 28},
            {"id": "u2", "label": "@citypulse", "group": "user", "risk": 72, "size": 20},
            {"id": "u3", "label": "@factchecknow", "group": "user", "risk": 41, "size": 18},
            {"id": "p1", "label": "Claim post", "group": "post", "risk": 88, "size": 24},
            {"id": "p2", "label": "Shared repost", "group": "post", "risk": 75, "size": 18},
            {"id": "h1", "label": "#EmergencyAlert", "group": "hashtag", "risk": 66, "size": 16},
        ],
        "edges": [
            {"source": "u1", "target": "p1", "type": "shares"},
            {"source": "u2", "target": "p1", "type": "replies"},
            {"source": "u1", "target": "p2", "type": "repost"},
            {"source": "p1", "target": "h1", "type": "mentions"},
            {"source": "p1", "target": "u3", "type": "quotes"},
        ],
        "centrality": {
            "@viralwatch": 0.81,
            "@citypulse": 0.58,
            "@factchecknow": 0.31,
        },
    }


def build_propagation() -> dict[str, Any]:
    return {
        "timeline": [
            {"time": "10:00", "posts": 5},
            {"time": "11:00", "posts": 21},
            {"time": "12:00", "posts": 86},
            {"time": "13:00", "posts": 304},
            {"time": "14:00", "posts": 890},
        ],
        "velocity": "Rapidly spreading",
        "cascade_size": 890,
        "peak_window": "13:00-14:00",
    }


def build_demo_analysis(claim_input: ClaimInput) -> InvestigationResult:
    text = _clean_text(claim_input.text)
    claims = extract_claims(text)
    primary_claim = claims[0]
    verdict, confidence, reason, uncertainty, risk_score = score_claim(text)

    evidence_items = build_evidence_items(primary_claim)
    claims_result = [
        ClaimResult(
            claim=primary_claim,
            evidence=evidence_items,
            prediction=verdict,
            confidence=confidence,
            reason=reason,
        )
    ]

    return InvestigationResult(
        investigation_id=f"INV-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{len(claims):03d}",
        claim=text,
        verdict=verdict,
        risk_score=risk_score,
        credibility=100 - risk_score,
        confidence=round(confidence * 100),
        uncertainty=round(uncertainty * 100),
        evidence_quality=91,
        propagation_risk="HIGH",
        network_coordination="SUSPICIOUS",
        media_consistency="LOW",
        primary_reason=reason,
        recommendation="Do not share this content without independent verification.",
        claims=claims_result,
        social_graph=build_graph_payload(),
        propagation=build_propagation(),
        explanation={
            "positive_signals": ["Evidence contradiction", "Rapid propagation", "High coordination", "Sensational language"],
            "negative_signals": ["Source reliability is low", "Visual mismatch", "Repeated wording in suspicious accounts"],
            "feature_importance": {
                "Evidence contradiction": 31,
                "Sensational language": 18,
                "Propagation burst": 15,
                "Image mismatch": 12,
                "Source reliability": 16,
            },
        },
        evidence=evidence_items,
        model_scores={
            "text_model": round(confidence, 4),
            "evidence_score": 0.81,
            "propagation_score": 0.78,
            "graph_score": 0.72,
            "multimodal_score": 0.51,
        },
        demo_data=True,
    )


def available_dashboard() -> dict[str, Any]:
    return {
        "total_analyses": 1824,
        "fake_suspicious": 724,
        "verified": 631,
        "unverified": 469,
        "high_risk_claims": 218,
        "manipulated_media": 143,
        "trending_misinformation": 19,
        "network_risk_score": 78,
        "recent_investigations": [
            {"id": "INV-2026-000118", "status": "LIKELY FALSE", "claim": "Government announced a complete shutdown of all digital payments.", "risk": 84},
            {"id": "INV-2026-000119", "status": "UNVERIFIED", "claim": "A viral video shows a flood crisis in a city never hit by storms.", "risk": 62},
            {"id": "INV-2026-000120", "status": "MISLEADING", "claim": "A celebrity health cure is being suppressed by authorities.", "risk": 71},
        ],
    }


def model_performance() -> list[dict[str, Any]]:
    report_path = Path(__file__).resolve().parents[3] / "reports" / "liar_800_evaluation.json"
    if not report_path.is_file():
        return []

    report = json.loads(report_path.read_text(encoding="utf-8"))
    metrics = report["test_metrics"]
    return [
        {
            "model": report["model"],
            "accuracy": metrics["accuracy"],
            "precision": metrics["macro_precision"],
            "recall": metrics["macro_recall"],
            "f1": metrics["macro_f1"],
            "auc": metrics["macro_roc_auc_ovr"],
        }
    ]


def trend_claims() -> list[dict[str, Any]]:
    return [
        {"claim": "Emergency order bans all online transactions in the district.", "risk": 92, "velocity": "Viral", "posts": 1290, "users": 436, "community_count": 5, "status": "Evidence contradicts"},
        {"claim": "A new miracle treatment is endorsed by health officials.", "risk": 78, "velocity": "Rapid", "posts": 810, "users": 302, "community_count": 4, "status": "Limited verification"},
        {"claim": "Authorities are hiding a major cyber-attack from the public.", "risk": 81, "velocity": "Rapid", "posts": 954, "users": 349, "community_count": 6, "status": "Sensitive narrative"},
    ]


def research_analytics() -> dict[str, Any]:
    return {
        "dataset_statistics": {
            "entries": 800,
            "train": 640,
            "validation": 80,
            "test": 80,
            "classes": 6,
            "source": "LIAR benchmark",
            "languages": ["English"],
        },
    }


def demo_investigations() -> list[dict[str, Any]]:
    return [
        {
            "id": "INV-2026-000118",
            "claim": "Government announced a complete shutdown of all digital payments.",
            "status": "LIKELY FALSE",
            "risk": 84,
            "confidence": 89,
            "evidence": 91,
            "platform": "X",
            "category": "Financial scam"
        },
        {
            "id": "INV-2026-000119",
            "claim": "A viral image shows a city under water despite no rainfall warning.",
            "status": "MISLEADING",
            "risk": 67,
            "confidence": 74,
            "evidence": 76,
            "platform": "Facebook",
            "category": "Disaster misinformation"
        },
        {
            "id": "INV-2026-000120",
            "claim": "A secret medical cure is being hidden by the authorities.",
            "status": "SUSPICIOUS",
            "risk": 74,
            "confidence": 81,
            "evidence": 72,
            "platform": "WhatsApp",
            "category": "Health misinformation"
        },
    ]
