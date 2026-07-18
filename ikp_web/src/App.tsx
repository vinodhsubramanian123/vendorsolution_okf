import { useState, useEffect } from 'react';
import axios from 'axios';
import { Sidebar } from './components/Sidebar';
import { SolutionSynthesis } from './components/SolutionSynthesis';
import { PlatformDashboard } from './components/PlatformDashboard';
import { BoqValidation } from './components/BoqValidation';
import { SemanticSearch } from './components/SemanticSearch';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export default function App() {
  const [activeTab, setActiveTab] = useState<'query' | 'dashboard' | 'boq' | 'search'>('query');
  const [status, setStatus] = useState<any>(null);
  
  useEffect(() => {
    fetchStatus();
  }, []);

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${API_BASE}/status`);
      setStatus(res.data);
    } catch (error) {
      console.error('Failed to fetch status:', error);
    }
  };

  return (
    <div className="app-container">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <div className="main-content">
        {status && status.repository_seeded === false && (
          <div className="repo-empty-banner" role="alert" style={{
            background: '#fff3cd', color: '#664d03', border: '1px solid #ffe69c',
            borderRadius: '6px', padding: '10px 14px', margin: '0 0 16px 0',
            fontSize: '14px',
          }}>
            The knowledge repository is empty -- queries, search, and the
            dashboard will return no results until it's seeded. Run{' '}
            <code>./scripts/bootstrap.sh</code> (see SETUP.md) and reload.
          </div>
        )}
        {activeTab === 'query' && <SolutionSynthesis />}
        {activeTab === 'dashboard' && <PlatformDashboard status={status} />}
        {activeTab === 'boq' && <BoqValidation />}
        {activeTab === 'search' && <SemanticSearch />}
      </div>
    </div>
  );
}
