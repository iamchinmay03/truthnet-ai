import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function TrendingPage() {
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    api.trending().then(setItems).catch(() => setItems([]));
  }, []);

  return (
    <div className="page">
      <header className="header">
        <div>
          <h1>Trending Claims</h1>
          <p>Claims ranked by circulation velocity and network spread.</p>
        </div>
      </header>

      <section className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Claim</th>
              <th>Risk</th>
              <th>Velocity</th>
              <th>Posts</th>
              <th>Users</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.claim}>
                <td>{item.claim}</td>
                <td>{item.risk}</td>
                <td>{item.velocity}</td>
                <td>{item.posts}</td>
                <td>{item.users}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
