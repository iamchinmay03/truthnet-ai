import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function InvestigationPage() {
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    api.investigations().then(setItems).catch(() => setItems([]));
  }, []);

  return (
    <div className="page">
      <header className="header">
        <div>
          <h1>Investigations</h1>
          <p>Recent case files and incident snapshots</p>
        </div>
      </header>

      <section className="card">
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Claim</th>
              <th>Platform</th>
              <th>Status</th>
              <th>Risk</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.claim}</td>
                <td>{item.platform}</td>
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
