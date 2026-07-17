import { useState } from 'react';
import axios from 'axios';
import { Database } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export function SemanticSearch() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearchLoading, setIsSearchLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim() || isSearchLoading) return;
    
    setIsSearchLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/search`, { query: searchQuery });
      setSearchResults(res.data.results);
    } catch (error) {
      console.error('Failed to search:', error);
    } finally {
      setIsSearchLoading(false);
    }
  };

  return (
    <>
      <header>
        <h1>Semantic Search</h1>
        <p>Search the vector database for rules, components, and documentation.</p>
      </header>
      
      <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '12px' }}>
          <input
            type="text"
            className="glass-input"
            placeholder="e.g. Memory configuration rules for DL380"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            disabled={isSearchLoading}
          />
          <button type="submit" className="btn-primary" disabled={isSearchLoading || !searchQuery.trim()}>
            <Database size={18} /> Search
          </button>
        </form>
        
        {searchResults.length > 0 && (
          <div style={{ marginTop: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {searchResults.map((res: any, i: number) => (
              <div key={i} style={{ padding: '16px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', border: '1px solid var(--border)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span style={{ fontWeight: 'bold', color: 'var(--primary)' }}>{res.title || res.id}</span>
                  <span style={{ fontSize: '0.8rem', background: 'rgba(255,255,255,0.1)', padding: '2px 8px', borderRadius: '12px' }}>
                    Score: {(res.score * 100).toFixed(1)}%
                  </span>
                </div>
                <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '8px' }}>
                  <span style={{ textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '1px', border: '1px solid var(--border)', padding: '2px 6px', borderRadius: '4px', marginRight: '8px' }}>
                    {res.type}
                  </span>
                  {res.id}
                </div>
                <div style={{ fontSize: '0.95rem', lineHeight: '1.5' }}>
                  {res.text}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
