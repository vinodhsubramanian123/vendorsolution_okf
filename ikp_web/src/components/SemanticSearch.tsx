import { useState } from 'react';
import axios from 'axios';
import { Database } from 'lucide-react';
import type { SearchResult } from '../types/api';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export function SemanticSearch() {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const [filterVendor, setFilterVendor] = useState('');
  const [filterGeneration, setFilterGeneration] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isSearchLoading, setIsSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim() || isSearchLoading) return;
    
    setIsSearchLoading(true);
    try {
      const filter_metadata: Record<string, string> = {};
      if (filterCategory) filter_metadata.category = filterCategory;
      if (filterVendor) filter_metadata.vendor = filterVendor;
      if (filterGeneration) filter_metadata.generation = filterGeneration;

      const payload = { 
        query: searchQuery, 
        filter_metadata: Object.keys(filter_metadata).length > 0 ? filter_metadata : undefined 
      };
      const res = await axios.post(`${API_BASE}/search`, payload);
      setSearchResults(res.data.results);
      setSearchError(null);
    } catch (error: any) {
      console.error('Failed to search:', error);
      setSearchError(error.response?.data?.detail || 'Search failed. Please try again later.');
    } finally {
      setIsSearchLoading(false);
    }
  };

  // Group results by type
  const groupedResults = searchResults.reduce((acc: Record<string, SearchResult[]>, res: SearchResult) => {
    const type = res.type || 'Unknown';
    if (!acc[type]) acc[type] = [];
    acc[type].push(res);
    return acc;
  }, {});

  return (
    <>
      <header>
        <h1>Semantic Search</h1>
        <p>Search the vector database for rules, components, and documentation.</p>
      </header>
      
      <div style={{ display: 'flex', gap: '24px' }}>
        {/* Sidebar Filter Panel */}
        <div className="glass-panel" style={{ width: '250px', display: 'flex', flexDirection: 'column', gap: '16px', height: 'fit-content' }}>
          <h3 style={{ fontSize: '1.1rem', margin: 0, color: 'var(--text-main)' }}>Filters</h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label htmlFor="filter-category" style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Category</label>
            <input id="filter-category" type="text" className="glass-input" placeholder="e.g. Memory" value={filterCategory} onChange={e => setFilterCategory(e.target.value)} />
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label htmlFor="filter-vendor" style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Vendor</label>
            <input id="filter-vendor" type="text" className="glass-input" placeholder="e.g. HPE" value={filterVendor} onChange={e => setFilterVendor(e.target.value)} />
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label htmlFor="filter-generation" style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Generation</label>
            <input id="filter-generation" type="text" className="glass-input" placeholder="e.g. Gen11" value={filterGeneration} onChange={e => setFilterGeneration(e.target.value)} />
          </div>
        </div>
        
        {/* Main Content */}
        <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <form onSubmit={handleSearch} style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label htmlFor="semantic-query" style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>Search Query</label>
            <div style={{ display: 'flex', gap: '12px' }}>
              <input
                id="semantic-query"
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
            </div>
          </form>

        {searchError && (
          <div style={{ padding: '16px', borderRadius: '8px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', color: '#ef4444', display: 'flex', alignItems: 'center', gap: '8px' }}>
            {searchError}
          </div>
        )}
        
        {searchResults.length > 0 && !searchError && (
          <div style={{ marginTop: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {Object.keys(groupedResults).sort().map(type => (
              <div key={type}>
                <h2 style={{ fontSize: '1.2rem', marginBottom: '12px', color: 'var(--primary)', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>
                  {type} ({groupedResults[type].length})
                </h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {groupedResults[type].map((res: SearchResult, i: number) => (
                    <div key={i} style={{ padding: '16px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', border: '1px solid var(--border)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                        <span style={{ fontWeight: 'bold', color: 'var(--text-main)' }}>{res.title || res.id}</span>
                        <span style={{ fontSize: '0.8rem', background: 'rgba(255,255,255,0.1)', padding: '2px 8px', borderRadius: '12px' }}>
                          Score: {(res.score * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '8px' }}>
                        ID: {res.id}
                      </div>
                      <div style={{ fontSize: '0.95rem', lineHeight: '1.5' }}>
                        {res.text}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
        </div>
      </div>
    </>
  );
}
