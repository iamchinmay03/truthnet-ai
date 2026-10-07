import { FormEvent, useState } from 'react';
import { api } from '../services/api';

export default function NewInvestigationPage() {
  const [text, setText] = useState('Government has banned all online payments from tomorrow and banks will remain closed for seven days.');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    try {
      const response = await api.analysis({ text });
      setResult(response);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="header">
        <div>
          <h1>New Investigation</h1>
          <p>Analyze a claim using text, evidence, graph and propagation checks.</p>
        </div>
      </header>

      <section className="report-card">
        <div className="card form-panel">
          <form onSubmit={handleSubmit}>
            <label htmlFor="claim">Claim / social media post</label>
            <textarea id="claim" value={text} onChange={(e) => setText(e.target.value)} placeholder="Paste a social claim, article snippet, or forwarded message..." />
            <button type="submit" disabled={loading}>{loading ? 'Analyzing…' : 'Submit investigation'}</button>
          </form>
        </div>

        <div className="card result-box">
          {result ? (
            <>
              <div className="verdict-badge">{result.verdict}</div>
              <div className="metric-row"><span>Risk</span><strong>{result.risk_score}/100</strong></div>
              <div className="metric-row"><span>Credibility</span><strong>{result.credibility}/100</strong></div>
              <div className="metric-row"><span>Confidence</span><strong>{result.confidence}%</strong></div>
              <div className="metric-row"><span>Evidence Quality</span><strong>{result.evidence_quality}/100</strong></div>
              <div className="metric-row"><span>Recommendation</span><strong>{result.recommendation}</strong></div>
              <p className="stat-foot">The text verdict uses the trained LIAR classifier. Evidence and propagation panels are illustrative demo data.</p>
            </>
          ) : (
            <div>
              <h3>Ready for analysis</h3>
              <p>The trained text classifier screens the claim. Evidence and network signals are illustrative demo data, not live verification.</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
