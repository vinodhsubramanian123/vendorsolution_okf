import { useState, useEffect } from 'react';
import axios from 'axios';
import { CheckCircle, AlertTriangle, XCircle, Search } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

type Evidence = {
  source_id: string;
  confidence: string;
  description?: string;
  original_text_snippet?: string;
};

type ReviewItem = {
  id: string;
  title: string;
  type: string;
  confidence: string;
  description: string;
  evidence: Evidence[];
};

export function ValidationPortal() {
  const [queue, setQueue] = useState<ReviewItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [approvingId, setApprovingId] = useState<string | null>(null);

  useEffect(() => {
    fetchQueue();
  }, []);

  const fetchQueue = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/review-queue`);
      setQueue(res.data.queue || []);
    } catch (err) {
      console.error('Failed to fetch review queue', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id: string) => {
    setApprovingId(id);
    try {
      await axios.post(`${API_BASE}/review-queue/approve`, { object_id: id });
      // Remove from queue
      setQueue(queue.filter(item => item.id !== id));
    } catch (err) {
      console.error('Failed to approve', err);
      alert('Failed to approve object. Check console for details.');
    } finally {
      setApprovingId(null);
    }
  };

  return (
    <>
      <header>
        <h1>Validation Portal</h1>
        <p>Human-in-the-Loop review for low-confidence AI extractions.</p>
      </header>
      
      <div className="glass-panel" style={{ flex: 1, overflowY: 'auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <h2 style={{ margin: 0, fontSize: '1.2rem', color: 'var(--primary)' }}>
            Pending Review ({queue.length})
          </h2>
          <button onClick={fetchQueue} className="btn-secondary">
            Refresh Queue
          </button>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
            Loading review queue...
          </div>
        ) : queue.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
            <CheckCircle size={48} style={{ opacity: 0.5, marginBottom: '16px' }} />
            <p>Queue is empty. All knowledge is fully verified.</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {queue.map(item => (
              <div key={item.id} style={{ 
                background: 'rgba(0,0,0,0.2)', 
                border: '1px solid var(--border)', 
                borderRadius: '8px',
                padding: '20px'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                      <span style={{ 
                        background: 'rgba(255, 204, 0, 0.1)', 
                        color: '#ffcc00', 
                        padding: '2px 8px', 
                        borderRadius: '4px', 
                        fontSize: '0.75rem', 
                        textTransform: 'uppercase',
                        letterSpacing: '1px'
                      }}>
                        {item.confidence} Confidence
                      </span>
                      <span style={{ 
                        border: '1px solid var(--border)', 
                        padding: '2px 8px', 
                        borderRadius: '4px', 
                        fontSize: '0.75rem', 
                        textTransform: 'uppercase',
                        color: 'var(--text-muted)'
                      }}>
                        {item.type}
                      </span>
                    </div>
                    <h3 style={{ margin: '0 0 8px 0', fontSize: '1.1rem' }}>{item.title}</h3>
                    <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--text-muted)' }}>ID: {item.id}</p>
                  </div>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button 
                      className="btn-primary" 
                      onClick={() => handleApprove(item.id)}
                      disabled={approvingId === item.id}
                      style={{ background: 'rgba(16, 185, 129, 0.2)', color: '#10b981', borderColor: '#10b981' }}
                    >
                      {approvingId === item.id ? 'Approving...' : 'Approve'}
                    </button>
                  </div>
                </div>

                <div style={{ marginBottom: '16px', background: 'rgba(0,0,0,0.3)', padding: '12px', borderRadius: '6px' }}>
                  <strong>Description/Rule:</strong>
                  <p style={{ margin: '8px 0 0 0', lineHeight: 1.5 }}>{item.description}</p>
                </div>

                {item.evidence && item.evidence.length > 0 && (
                  <div>
                    <strong style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Citations & Context:</strong>
                    <div style={{ marginTop: '8px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      {item.evidence.map((ev, idx) => (
                        <div key={idx} style={{ 
                          borderLeft: '3px solid var(--primary)', 
                          padding: '8px 12px',
                          background: 'rgba(255, 255, 255, 0.05)',
                          fontSize: '0.85rem'
                        }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px', color: 'var(--text-muted)' }}>
                            <span>Source: {ev.source_id}</span>
                            <span>{ev.confidence} Match</span>
                          </div>
                          {ev.original_text_snippet && (
                            <p style={{ margin: '8px 0 0 0', fontStyle: 'italic', color: '#ddd' }}>
                              "{ev.original_text_snippet}"
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
