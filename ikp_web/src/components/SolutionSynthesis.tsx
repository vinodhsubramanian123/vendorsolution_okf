import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, CheckCircle2, Component } from 'lucide-react';
import type { SolutionCandidate } from '../types/api';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export type ChatMessage = {
  id: string;
  role: 'user' | 'system';
  content: string;
  type: 'text' | 'bom' | 'loading';
  data?: SolutionCandidate;
};

export function SolutionSynthesis() {
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
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    const query = input;
    setInput('');
    
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
      setMessages(prev => prev.filter(m => m.type !== 'loading'));
      
      if (res.data.candidates && res.data.candidates.length > 0) {
        const topCandidate: SolutionCandidate = res.data.candidates[0];
        setMessages(prev => [...prev, {
          id: Date.now().toString(),
          role: 'system',
          content: `I've designed a solution optimized for ${topCandidate.profile || 'your requirements'}. It includes ${topCandidate.components.length} components.`,
          type: 'bom',
          data: topCandidate
        }]);
      } else {
        setMessages(prev => [...prev, {
          id: Date.now().toString(),
          role: 'system',
          content: "I couldn't generate a valid BOM for those requirements. Try adjusting your constraints.",
          type: 'text'
        }]);
      }
    } catch (error: any) {
      console.error('Failed to generate solution:', error);
      setMessages(prev => prev.filter(m => m.type !== 'loading'));
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        role: 'system',
        content: error.response?.data?.detail || "An error occurred while connecting to the engine. Please try again.",
        type: 'text'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
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
  );
}
