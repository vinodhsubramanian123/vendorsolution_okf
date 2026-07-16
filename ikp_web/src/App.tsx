import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Database, Server, Component, Send, Cpu, LayoutTemplate, ShieldAlert, CheckCircle2 } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

type ChatMessage = {
  id: string;
  role: 'user' | 'system';
  content: string;
  type: 'text' | 'bom' | 'loading';
  data?: any;
};

export default function App() {
  const [activeTab, setActiveTab] = useState<'query' | 'dashboard' | 'boq' | 'search'>('query');
  const [status, setStatus] = useState<any>(null);
  
  // BOQ state
  const [boqInput, setBoqInput] = useState('');
  const [boqResult, setBoqResult] = useState<any>(null);
  const [isBoqLoading, setIsBoqLoading] = useState(false);
  
  // Search state
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearchLoading, setIsSearchLoading] = useState(false);
  
  // Chat state
  const [messages, setMessages] = useState<ChatMessage[]>([{
    id: '1',
    role: 'system',
    content: 'Welcome to the IKP AI Reasoning Engine. What infrastructure do you need to build today?',
    type: 'text'
  }]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchStatus();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${API_BASE}/status`);
      setStatus(res.data);
    } catch (error) {
      console.error('Failed to fetch status:', error);
    }
  };

  const handleBoqValidation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!boqInput.trim() || isBoqLoading) return;
    
    setIsBoqLoading(true);
    try {
      // Split by commas or newlines
      const components = boqInput.split(/[\n,]+/).map(s => s.trim()).filter(Boolean);
      const res = await axios.post(`${API_BASE}/boq/validate`, { components });
      setBoqResult(res.data);
    } catch (error) {
      console.error('Failed to validate BOQ:', error);
    } finally {
      setIsBoqLoading(false);
    }
  };
  
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      if (content) {
        setBoqInput(content);
      }
    };
    reader.readAsText(file);
  };
  
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

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    const query = input;
    setInput('');
    
    // Add user message
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: query,
      type: 'text'
    };
    
    const loadingMsg: ChatMessage = {
      id: (Date.now() + 1).toString(),
      role: 'system',
      content: 'Analyzing requirements and synthesizing solution...',
      type: 'loading'
    };
    
    setMessages(prev => [...prev, userMsg, loadingMsg]);
    setIsLoading(true);
    
    try {
      const res = await axios.post(`${API_BASE}/query`, { query });
      
      // Remove loading message
      setMessages(prev => prev.filter(m => m.type !== 'loading'));
      
      if (res.data.candidates && res.data.candidates.length > 0) {
        const topCandidate = res.data.candidates[0];
        
        setMessages(prev => [...prev, {
          id: Date.now().toString(),
          role: 'system',
          content: `Generated optimal configuration (${topCandidate.profile} profile).`,
          type: 'bom',
          data: topCandidate
        }]);
      } else {
        setMessages(prev => [...prev, {
          id: Date.now().toString(),
          role: 'system',
          content: 'I could not find a valid solution matching those requirements.',
          type: 'text'
        }]);
      }
    } catch (error) {
      setMessages(prev => prev.filter(m => m.type !== 'loading'));
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        role: 'system',
        content: 'Error communicating with the reasoning engine.',
        type: 'text'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
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
            <Database size={20} /> Semantic Search
          </button>
        </div>
        
        <div style={{ marginTop: 'auto', borderTop: '1px solid var(--border)', paddingTop: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: 'var(--text-muted)' }}>
            <Database size={16} />
            <span style={{ fontSize: '0.9rem' }}>Vector Store Connected</span>
          </div>
        </div>
      </div>
      
      {/* Main Content */}
      <div className="main-content">
        {activeTab === 'query' && (
          <>
            <header>
              <h1>Solution Synthesis</h1>
              <p>Natural language AI reasoning engine for infrastructure design.</p>
            </header>
            
            <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <div className="chat-container">
                {messages.map((msg) => (
                  <div key={msg.id} className={`chat-bubble ${msg.role === 'user' ? 'chat-user' : 'chat-system'}`}>
                    {msg.type === 'loading' ? (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div className="animate-pulse" style={{ width: '8px', height: '8px', background: 'var(--primary)', borderRadius: '50%' }} />
                        <span>{msg.content}</span>
                      </div>
                    ) : (
                      <div>
                        {msg.role === 'system' && <div style={{ marginBottom: '8px', fontSize: '0.8rem', color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '1px' }}>IKP Engine</div>}
                        <div style={{ lineHeight: '1.5' }}>{msg.content}</div>
                        
                        {/* Render BOM if available */}
                        {msg.type === 'bom' && msg.data && (
                          <div style={{ marginTop: '16px', background: 'rgba(0,0,0,0.3)', padding: '16px', borderRadius: '8px', border: '1px solid var(--border)' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                              <CheckCircle2 color="var(--primary)" size={20} />
                              <h3 style={{ margin: 0, color: 'var(--primary)' }}>Validated Configuration</h3>
                            </div>
                            
                            <table className="data-table">
                              <thead>
                                <tr>
                                  <th>Component ID</th>
                                </tr>
                              </thead>
                              <tbody>
                                {msg.data.components.map((comp: string, i: number) => (
                                  <tr key={i}>
                                    <td style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                      <Component size={16} color="var(--text-muted)" />
                                      {comp}
                                    </td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                            
                            <div style={{ marginTop: '16px' }}>
                              <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '8px', textTransform: 'uppercase' }}>Reasoning Chain</h4>
                              <ul style={{ listStyleType: 'none', padding: 0, margin: 0, fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                                {msg.data.reasoning_chain.map((step: string, i: number) => (
                                  <li key={i} style={{ marginBottom: '6px', display: 'flex', gap: '8px' }}>
                                    <span style={{ color: 'var(--secondary)' }}>{'>'}</span> {step}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>
              
              <form onSubmit={handleQuery} style={{ display: 'flex', gap: '12px', marginTop: '16px' }}>
                <input
                  type="text"
                  className="glass-input"
                  placeholder="e.g. I need an AI server with a GPU and 1TB of NVMe..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  disabled={isLoading}
                />
                <button type="submit" className="btn-primary" disabled={isLoading || !input.trim()}>
                  <Send size={18} />
                </button>
              </form>
            </div>
          </>
        )}
        
        {activeTab === 'dashboard' && status && (
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
        )}
        
        {activeTab === 'boq' && (
          <>
            <header>
              <h1>BOQ Validation</h1>
              <p>Paste a comma-separated list of SKUs to test them against the canonical rules engine.</p>
            </header>
            
            <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <form onSubmit={handleBoqValidation} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <label htmlFor="csv-upload" className="btn-secondary" style={{ cursor: 'pointer', padding: '8px 16px', background: 'rgba(255,255,255,0.1)', borderRadius: '8px', border: '1px solid var(--border)', color: 'var(--text-main)' }}>
                    Upload CSV
                    <input 
                      id="csv-upload" 
                      type="file" 
                      accept=".csv,.txt" 
                      style={{ display: 'none' }} 
                      onChange={handleFileUpload} 
                    />
                  </label>
                  <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Or paste SKUs below (separated by commas or newlines)</span>
                </div>
                
                <textarea
                  className="glass-input"
                  style={{ minHeight: '150px', resize: 'vertical' }}
                  placeholder="e.g. P52562-B21, P49023-B21"
                  value={boqInput}
                  onChange={(e) => setBoqInput(e.target.value)}
                  disabled={isBoqLoading}
                />
                <button type="submit" className="btn-primary" disabled={isBoqLoading || !boqInput.trim()}>
                  {isBoqLoading ? 'Validating...' : 'Validate BOQ'}
                </button>
              </form>
              
              {boqResult && (
                <div style={{ marginTop: '24px' }}>
                  <div style={{ 
                    padding: '16px', 
                    borderRadius: '8px', 
                    marginBottom: '16px',
                    background: boqResult.is_valid ? 'rgba(34, 197, 94, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                    border: `1px solid ${boqResult.is_valid ? '#22c55e' : '#ef4444'}`
                  }}>
                    <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
                      {boqResult.is_valid ? <CheckCircle2 color="#22c55e" /> : <ShieldAlert color="#ef4444" />}
                      {boqResult.is_valid ? 'Validation Passed' : 'Validation Failed'}
                    </h3>
                  </div>
                  
                  {boqResult.rule_evaluations && boqResult.rule_evaluations.length > 0 && (
                    <div style={{ marginTop: '16px' }}>
                      <h4>Rule Evaluations</h4>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '12px' }}>
                        {boqResult.rule_evaluations.map((rule: any, i: number) => (
                          <div key={i} style={{ 
                            padding: '12px', 
                            borderRadius: '6px', 
                            background: 'rgba(0,0,0,0.2)',
                            borderLeft: `4px solid ${rule.status === 'PASS' ? '#22c55e' : '#ef4444'}`
                          }}>
                            <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>{rule.title}</div>
                            <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Status: {rule.status}</div>
                            {rule.message && <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Details: {rule.message}</div>}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </>
        )}
        
        {activeTab === 'search' && (
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
        )}
      </div>
    </div>
  );
}
