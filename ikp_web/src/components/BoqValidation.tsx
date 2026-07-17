import { useState } from 'react';
import axios from 'axios';
import { CheckCircle2, ShieldAlert } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export function BoqValidation() {
  const [boqInput, setBoqInput] = useState('');
  const [boqResult, setBoqResult] = useState<any>(null);
  const [isBoqLoading, setIsBoqLoading] = useState(false);

  const handleBoqValidation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!boqInput.trim() || isBoqLoading) return;
    
    setIsBoqLoading(true);
    try {
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

  return (
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
  );
}
