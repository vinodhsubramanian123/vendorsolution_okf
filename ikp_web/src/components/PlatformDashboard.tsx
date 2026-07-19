import type { StatusResponse, IntegrationsResponse } from '../types/api';
import { Activity, Database, Brain } from 'lucide-react';

export function PlatformDashboard({ status, integrations }: { status: StatusResponse | any, integrations: IntegrationsResponse | null }) {
  if (!status) return null;
  
  return (
    <>
      <header>
        <h1>Platform Dashboard</h1>
        <p>Real-time statistics from the underlying Knowledge Graph.</p>
      </header>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '40px' }}>
          <div style={{ fontSize: '4rem', fontWeight: 'bold', color: 'var(--primary)' }}>
            {status.stats?.total_nodes || 0}
          </div>
          <div style={{ color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>
            Total Nodes
          </div>
        </div>
        
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '40px' }}>
          <div style={{ fontSize: '4rem', fontWeight: 'bold', color: 'var(--secondary)' }}>
            {status.stats?.total_edges || 0}
          </div>
          <div style={{ color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>
            Relationships
          </div>
        </div>
      </div>
      
      {integrations && (
        <div className="glass-panel" style={{ marginTop: '24px' }}>
          <h2>Integrations Health</h2>
          <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
            <div style={{ flex: 1, minWidth: '200px', padding: '16px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', borderLeft: `4px solid ${integrations.integrations.llm.status === 'Available' ? '#22c55e' : '#ef4444'}` }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <Brain size={20} color={integrations.integrations.llm.status === 'Available' ? '#22c55e' : '#ef4444'} />
                <strong style={{ fontSize: '1.1rem' }}>LLM</strong>
              </div>
              <div style={{ color: 'var(--text-muted)' }}>{integrations.integrations.llm.name}</div>
              <div style={{ marginTop: '8px', fontWeight: 'bold', color: integrations.integrations.llm.status === 'Available' ? '#22c55e' : '#ef4444' }}>{integrations.integrations.llm.status}</div>
            </div>

            <div style={{ flex: 1, minWidth: '200px', padding: '16px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', borderLeft: `4px solid ${integrations.integrations.vector_index.status === 'Available' ? '#22c55e' : '#ef4444'}` }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <Database size={20} color={integrations.integrations.vector_index.status === 'Available' ? '#22c55e' : '#ef4444'} />
                <strong style={{ fontSize: '1.1rem' }}>Vector Index</strong>
              </div>
              <div style={{ color: 'var(--text-muted)' }}>{integrations.integrations.vector_index.name}</div>
              <div style={{ marginTop: '8px', fontWeight: 'bold', color: integrations.integrations.vector_index.status === 'Available' ? '#22c55e' : '#ef4444' }}>{integrations.integrations.vector_index.status}</div>
            </div>

            <div style={{ flex: 1, minWidth: '200px', padding: '16px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', borderLeft: `4px solid ${integrations.integrations.mcp.status === 'Configured' ? '#3b82f6' : '#94a3b8'}` }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <Activity size={20} color={integrations.integrations.mcp.status === 'Configured' ? '#3b82f6' : '#94a3b8'} />
                <strong style={{ fontSize: '1.1rem' }}>MCP Tools</strong>
              </div>
              <div style={{ color: 'var(--text-muted)' }}>{integrations.integrations.mcp.name}</div>
              <div style={{ marginTop: '8px', fontWeight: 'bold', color: integrations.integrations.mcp.status === 'Configured' ? '#3b82f6' : '#94a3b8' }}>{integrations.integrations.mcp.status}</div>
            </div>
          </div>
        </div>
      )}
      
      <div className="glass-panel" style={{ marginTop: '24px' }}>
        <h2>Products Overview</h2>
        <table className="data-table">
          <thead>
            <tr>
              <th>Platform ID</th>
              <th>SKUs</th>
              <th>Categories</th>
              <th>Rules</th>
            </tr>
          </thead>
          <tbody>
            {status.platforms && Object.entries(status.platforms).map(([id, p]: [string, any]) => (
              <tr key={id}>
                <td style={{ fontWeight: 'bold', color: 'var(--primary)' }}>{id}</td>
                <td>{p.skus}</td>
                <td>{p.categories}</td>
                <td>{p.rules}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="glass-panel" style={{ marginTop: '24px' }}>
        <h2>Objects by Type</h2>
        <table className="data-table">
          <thead>
            <tr>
              <th>Object Type</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            {status.stats?.type_counts && Object.entries(status.stats.type_counts).map(([type, count]) => (
              <tr key={type}>
                <td>{type}</td>
                <td>{count as number}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
