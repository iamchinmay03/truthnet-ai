const API_BASE = import.meta.env.VITE_API_URL || '';

async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  dashboard: () => fetchJson<any>('/api/dashboard'),
  investigations: () => fetchJson<any[]>('/api/investigations'),
  analysis: (payload: { text: string; url?: string; platform?: string; language?: string }) =>
    fetch(`${API_BASE}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }).then((res) => {
      if (!res.ok) throw new Error('Analysis failed');
      return res.json();
    }),
  trending: () => fetchJson<any[]>('/api/trending'),
  research: () => fetchJson<any>('/api/research'),
  performance: () => fetchJson<any[]>('/api/models/performance'),
};
