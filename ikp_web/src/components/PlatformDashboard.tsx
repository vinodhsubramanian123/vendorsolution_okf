export function PlatformDashboard({ status }: { status: any }) {
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
