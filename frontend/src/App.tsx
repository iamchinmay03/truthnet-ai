import { NavLink, Route, Routes } from 'react-router-dom';
import { BarChart3, BrainCircuit, FileSearch, LayoutDashboard, Network, Radar, ShieldAlert, TrendingUp } from 'lucide-react';
import DashboardPage from './pages/DashboardPage';
import InvestigationPage from './pages/InvestigationPage';
import NewInvestigationPage from './pages/NewInvestigationPage';
import ResearchPage from './pages/ResearchPage';
import TrendingPage from './pages/TrendingPage';

const navItems = [
  { label: 'Dashboard', to: '/', icon: LayoutDashboard },
  { label: 'New Investigation', to: '/investigate', icon: FileSearch },
  { label: 'Investigations', to: '/investigations', icon: ShieldAlert },
  { label: 'Social Network', to: '/network', icon: Network },
  { label: 'Propagation', to: '/trending', icon: TrendingUp },
  { label: 'Research', to: '/research', icon: BrainCircuit },
  { label: 'Reports', to: '/reports', icon: BarChart3 },
  { label: 'Media Analysis', to: '/media', icon: Radar },
];

function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">T</div>
          <div>
            <strong>TruthNet AI</strong>
            <small>Explainable intelligence</small>
          </div>
        </div>

        <nav className="nav">
          {navItems.map(({ label, to, icon: Icon }) => (
            <NavLink key={label} to={to} className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="main-panel">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/investigate" element={<NewInvestigationPage />} />
          <Route path="/investigations" element={<InvestigationPage />} />
          <Route path="/trending" element={<TrendingPage />} />
          <Route path="/research" element={<ResearchPage />} />
          <Route path="/network" element={<DashboardPage />} />
          <Route path="/reports" element={<DashboardPage />} />
          <Route path="/media" element={<DashboardPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
