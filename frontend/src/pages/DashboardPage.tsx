import { useEffect, useState } from 'react';
import { BarChart, Bar, CartesianGrid, PieChart, Pie, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { api } from '../services/api';

const pieColors = ['#60a5fa', '#34d399', '#fbbf24', '#fb7185'];

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState<any>(null);
  useEffect(() => {
    api.dashboard().then(setDashboard).catch(() => setDashboard({
      total_analyses: 0,
      fake_suspicious: 0,
      verified: 0,
      unverified: 0,
      high_risk_claims: 0,
      manipulated_media: 0,
      trending_misinformation: 0,
      network_risk_score: 0,
      recent_investigations: [],
    }));
  }, []);

  if (!dashboard) return <div className="page"><div className="card">Loading dashboard…</div></div>;

  const data = [
    { name: 'Fake / suspicious', value: dashboard.fake_suspicious },
    { name: 'Verified', value: dashboard.verified },
    { name: 'Unverified', value: dashboard.unverified },
  ];

  const riskTrend = [
    { name: 'Jan', value: 32 },
    { name: 'Feb', value: 37 },
    { name: 'Mar', value: 50 },
    { name: 'Apr', value: 58 },
    { name: 'May', value: 71 },
    { name: 'Jun', value: 79 },
  ];

  return (
    <div className="page">
      <header className="header">
        <div>
          <h1>Dashboard</h1>
          <p>TruthNet AI intelligence overview</p>
        </div>
      </header>

      <section className="grid">
        <div className="card stat-card"><span className="stat-label">Total analyses</span><span className="stat-value">{dashboard.total_analyses}</span><span className="stat-foot">Across all monitored networks</span></div>
        <div className="card stat-card"><span className="stat-label">Fake / suspicious</span><span className="stat-value">{dashboard.fake_suspicious}</span><span className="stat-foot">High-risk narratives flagged</span></div>
        <div className="card stat-card"><span className="stat-label">Verified content</span><span className="stat-value">{dashboard.verified}</span><span className="stat-foot">Strengthened by evidence checks</span></div>
        <div className="card stat-card"><span className="stat-label">Unverified</span><span className="stat-value">{dashboard.unverified}</span><span className="stat-foot">Awaiting independent verification</span></div>
        <div className="card stat-card"><span className="stat-label">Network risk score</span><span className="stat-value">{dashboard.network_risk_score}</span><span className="stat-foot">Derived from propagation and graph metrics</span></div>
        <div className="card stat-card"><span className="stat-label">Manipulated media</span><span className="stat-value">{dashboard.manipulated_media}</span><span className="stat-foot">Visual integrity alerts</span></div>
      </section>

      <section className="report-card">
        <div className="card">
          <h3>Distribution</h3>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={data} dataKey="value" nameKey="name" innerRadius={60} outerRadius={90} paddingAngle={4}>
                {data.map((_, index) => <Cell key={index} fill={pieColors[index % pieColors.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3>Risk trend</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={riskTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2b3a52" />
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip />
              <Bar dataKey="value" fill="#60a5fa" radius={[10, 10, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="card">
        <h3>Recent investigations</h3>
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Claim</th>
              <th>Status</th>
              <th>Risk</th>
            </tr>
          </thead>
          <tbody>
            {dashboard.recent_investigations.map((item: any) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.claim}</td>
                <td><span className="badge">{item.status}</span></td>
                <td>{item.risk}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
