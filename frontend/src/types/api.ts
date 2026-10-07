export type InvestigationSummary = {
  id: string;
  claim: string;
  status: string;
  risk: number;
  confidence: number;
  evidence: number;
  platform: string;
  category: string;
};

export type DashboardData = {
  total_analyses: number;
  fake_suspicious: number;
  verified: number;
  unverified: number;
  high_risk_claims: number;
  manipulated_media: number;
  trending_misinformation: number;
  network_risk_score: number;
  recent_investigations: Array<{ id: string; status: string; claim: string; risk: number }>;
};
