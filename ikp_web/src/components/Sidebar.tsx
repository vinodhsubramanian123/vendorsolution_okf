import { Database, Server, Cpu, LayoutTemplate, CheckCircle2, BookOpen, Search } from 'lucide-react';

interface SidebarProps {
  activeTab: 'query' | 'dashboard' | 'boq' | 'search' | 'review' | 'kt';
  setActiveTab: (tab: 'query' | 'dashboard' | 'boq' | 'search' | 'review' | 'kt') => void;
}

export function Sidebar({ activeTab, setActiveTab }: SidebarProps) {
  return (
    <div className="sidebar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{ background: 'var(--primary)', padding: '8px', borderRadius: '8px' }}>
          <Server color="#000" size={24} />
        </div>
        <div>
          <h2 style={{ marginBottom: 0, fontSize: '1.2rem' }}>IKP Portal</h2>
          <span style={{ color: 'var(--primary)', fontSize: '0.8rem' }}>v2.0 Enterprise</span>
        </div>
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <button 
          style={{
            background: activeTab === 'query' ? 'rgba(255,255,255,0.1)' : 'transparent',
            border: 'none',
            color: 'var(--text-main)',
            padding: '12px 16px',
            borderRadius: '8px',
            textAlign: 'left',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            fontSize: '1rem'
          }}
          onClick={() => setActiveTab('query')}
        >
          <Cpu size={20} /> Solution Synthesis
        </button>
        
        <button 
          style={{
            background: activeTab === 'dashboard' ? 'rgba(255,255,255,0.1)' : 'transparent',
            border: 'none',
            color: 'var(--text-main)',
            padding: '12px 16px',
            borderRadius: '8px',
            textAlign: 'left',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            fontSize: '1rem'
          }}
          onClick={() => setActiveTab('dashboard')}
        >
          <LayoutTemplate size={20} /> Graph Dashboard
        </button>
        
        <button 
          style={{
            background: activeTab === 'boq' ? 'rgba(255,255,255,0.1)' : 'transparent',
            border: 'none',
            color: 'var(--text-main)',
            padding: '12px 16px',
            borderRadius: '8px',
            textAlign: 'left',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            fontSize: '1rem'
          }}
          onClick={() => setActiveTab('boq')}
        >
          <CheckCircle2 size={20} /> BOQ Validation
        </button>
        
        <button 
          style={{
            background: activeTab === 'search' ? 'rgba(255,255,255,0.1)' : 'transparent',
            border: 'none',
            color: 'var(--text-main)',
            padding: '12px 16px',
            borderRadius: '8px',
            textAlign: 'left',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            fontSize: '1rem'
          }}
          onClick={() => setActiveTab('search')}
        >
          <Search size={20} /> Semantic Search
        </button>

        <button 
          style={{
            background: activeTab === 'kt' ? 'rgba(255,255,255,0.1)' : 'transparent',
            border: 'none',
            color: 'var(--text-main)',
            padding: '12px 16px',
            borderRadius: '8px',
            textAlign: 'left',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            fontSize: '1rem'
          }}
          onClick={() => setActiveTab('kt')}
        >
          <BookOpen size={20} /> Knowledge Transfer
        </button>

        <button 
          style={{
            background: activeTab === 'review' ? 'rgba(255,255,255,0.1)' : 'transparent',
            border: 'none',
            color: 'var(--text-main)',
            padding: '12px 16px',
            borderRadius: '8px',
            textAlign: 'left',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            fontSize: '1rem'
          }}
          onClick={() => setActiveTab('review')}
        >
          <CheckCircle2 size={20} /> Validation Portal
        </button>
      </div>
      
      <div style={{ marginTop: 'auto', borderTop: '1px solid var(--border)', paddingTop: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: 'var(--text-muted)' }}>
          <Database size={16} />
          <span style={{ fontSize: '0.9rem' }}>Vector Store Connected</span>
        </div>
      </div>
    </div>
  );
}
