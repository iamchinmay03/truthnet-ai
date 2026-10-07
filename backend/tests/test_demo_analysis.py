from app.schemas.analysis import ClaimInput
from app.services.demo_engine import build_demo_analysis


def test_demo_analysis_returns_risk_and_evidence():
    payload = ClaimInput(
        text="Government has banned all online payments from tomorrow and banks will remain closed for seven days.",
    )

    result = build_demo_analysis(payload)

    assert result.verdict in {"LIKELY FALSE", "MISLEADING", "PARTLY TRUE", "MOSTLY TRUE", "LIKELY TRUE", "UNVERIFIED"}
    assert 0 <= result.risk_score <= 100
    assert result.credibility == 100 - result.risk_score
    assert len(result.evidence) >= 1
    assert result.model_scores["text_model"] > 0
    assert result.demo_data is True
    assert "LIAR benchmark" in result.primary_reason
