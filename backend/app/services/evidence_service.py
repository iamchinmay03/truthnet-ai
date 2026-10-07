from __future__ import annotations


def authoritative_sources(claim: str) -> list[dict[str, str | float]]:
    return [
        {
            "title": "Official verification record",
            "publisher": "Government source",
            "date": "2026-01-12",
            "url": "https://example.gov/official-records",
            "relevance": 0.94,
            "direction": "contradicting",
            "summary": "The official record does not confirm the reported claim.",
        },
        {
            "title": "Independent audit and fact check",
            "publisher": "Research fact-checker",
            "date": "2026-01-14",
            "url": "https://example.org/audit",
            "relevance": 0.88,
            "direction": "contradicting",
            "summary": "The timing and scope described in the content are inconsistent with independent reporting.",
        },
        {
            "title": "Background context and timeline review",
            "publisher": "Policy analysis desk",
            "date": "2026-01-15",
            "url": "https://example.edu/timeline-review",
            "relevance": 0.73,
            "direction": "contextual",
            "summary": "The broader timeline indicates the claim is not supported by corroborating events.",
        },
    ]


def evidence_quality_score(sources: list[dict[str, object]]) -> int:
    if not sources:
        return 0
    return int(round(sum(float(item["relevance"]) for item in sources) / len(sources) * 100))
