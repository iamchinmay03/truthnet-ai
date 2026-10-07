from typing import Any, List, Optional

from pydantic import BaseModel, Field


class ClaimInput(BaseModel):
    text: str = Field(..., min_length=1)
    url: Optional[str] = None
    image_url: Optional[str] = None
    platform: Optional[str] = "unknown"
    language: Optional[str] = "en"
    dataset: Optional[dict[str, Any]] = None


class EvidenceItem(BaseModel):
    title: str
    publisher: str
    date: str
    url: str
    relevance: float
    direction: str
    summary: str


class ClaimResult(BaseModel):
    claim: str
    evidence: List[EvidenceItem]
    prediction: str
    confidence: float
    reason: str


class InvestigationResult(BaseModel):
    investigation_id: str
    claim: str
    verdict: str
    risk_score: int
    credibility: int
    confidence: float
    uncertainty: float
    evidence_quality: int
    propagation_risk: str
    network_coordination: str
    media_consistency: str
    primary_reason: str
    recommendation: str
    claims: List[ClaimResult]
    social_graph: dict[str, Any]
    propagation: dict[str, Any]
    explanation: dict[str, Any]
    evidence: List[EvidenceItem]
    model_scores: dict[str, float]
    demo_data: bool = True
