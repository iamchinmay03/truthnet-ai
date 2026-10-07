import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function ResearchPage() {
  const [performance, setPerformance] = useState<any[]>([]);
  const [research, setResearch] = useState<any>(null);

  useEffect(() => {
    Promise.all([api.performance(), api.research()]).then(([models, analytics]) => {
      setPerformance(models);
      setResearch(analytics);
    }).catch(() => {
      setPerformance([]);
      setResearch(null);
    });
  }, []);

  const dataset = research?.dataset_statistics;
  const percent = (value: number | null) => value == null ? 'N/A' : `${(value * 100).toFixed(1)}%`;

  return (
    <div className="page">
      <header className="header">
        <div>
          <h1>Research Analytics</h1>
          <p>Held-out performance for the locally trained LIAR benchmark classifier.</p>
        </div>
      </header>

      <section className="grid">
        <div className="card"><span className="stat-label">Dataset entries</span><span className="stat-value">{dataset?.entries ?? '--'}</span></div>
        <div className="card"><span className="stat-label">Training</span><span className="stat-value">{dataset?.train ?? '--'}</span></div>
        <div className="card"><span className="stat-label">Validation</span><span className="stat-value">{dataset?.validation ?? '--'}</span></div>
        <div className="card"><span className="stat-label">Held-out test</span><span className="stat-value">{dataset?.test ?? '--'}</span></div>
      </section>

      <section className="card">
        <h3>Model performance</h3>
        <table className="table">
          <thead>
            <tr>
              <th>Model</th>
              <th>Accuracy</th>
              <th>F1</th>
              <th>AUC</th>
            </tr>
          </thead>
          <tbody>
            {performance.map((item) => (
              <tr key={item.model}>
                <td>{item.model}</td>
                <td>{percent(item.accuracy)}</td>
                <td>{percent(item.f1)}</td>
                <td>{percent(item.auc)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <p className="stat-foot">Six-class statement rating benchmark. Results are from 80 held-out examples and should not be treated as proof of truth.</p>
    </div>
  );
}
