import { useState, useEffect } from 'react';
import axios from 'axios';
import { CheckCircle2, ShieldAlert } from 'lucide-react';

import type { BOQValidationResponse, ValidationMessage } from '../types/api';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export function BoqValidation() {
  const [boqInput, setBoqInput] = useState('');
  const [platformId, setPlatformId] = useState('');
  const [platforms, setPlatforms] = useState<any[]>([]);
  const [boqResult, setBoqResult] = useState<BOQValidationResponse | null>(null);
  const [isBoqLoading, setIsBoqLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');



  useEffect(() => {
    const fetchPlatforms = async () => {
      try {
        const res = await axios.get(`${API_BASE}/status`);
        if (res.data?.platforms) {
          const platformArray = Object.entries(res.data.platforms).map(([id, data]: [string, any]) => ({
            id,
            title: data.title
          }));
          setPlatforms(platformArray);
        }
      } catch (err) {
        console.error('Failed to fetch platforms:', err);
      }
    };
    fetchPlatforms();
  }, []);

  const handleBoqValidation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!boqInput.trim() || isBoqLoading) return;
    
    setIsBoqLoading(true);
    setErrorMsg('');
    try {
      const components = boqInput.split(/[\n,]+/).map(s => s.trim()).filter(Boolean);
      const res = await axios.post(`${API_BASE}/boq/validate`, {
        components,
        platform_id: platformId.trim() || undefined,
      });
      setBoqResult(res.data);
    } catch (error: any) {
      console.error('Failed to validate BOQ:', error);
      setErrorMsg(error.response?.data?.detail || 'Failed to connect to validation server. Please try again.');
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
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label htmlFor="boq-skus" style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>SKUs to Validate</label>
            <textarea
              id="boq-skus"
              className="glass-input"
              style={{ minHeight: '150px', resize: 'vertical' }}
              placeholder="e.g. P52562-B21, P49023-B21"
              value={boqInput}
              onChange={(e) => setBoqInput(e.target.value)}
              disabled={isBoqLoading}
            />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label htmlFor="boq-platform-id" style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>Target Platform (Optional)</label>
            <select
              id="boq-platform-id"
              className="glass-input"
              value={platformId}
              onChange={(e) => setPlatformId(e.target.value)}
              disabled={isBoqLoading}
            >
              <option value="">Auto-Detect from SKUs</option>
              {platforms.map(p => (
                <option key={p.id} value={p.id}>{p.title} ({p.id})</option>
              ))}
            </select>
          </div>
          <button type="submit" className="btn-primary" disabled={isBoqLoading || !boqInput.trim()}>
            {isBoqLoading ? 'Validating...' : 'Validate BOQ'}
          </button>
        </form>
        
        {errorMsg && (
          <div style={{ marginTop: '16px', padding: '16px', borderRadius: '8px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', color: '#ef4444', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldAlert size={20} />
            {errorMsg}
          </div>
        )}

        {!boqResult && !isBoqLoading && !errorMsg && (
          <div style={{ marginTop: '24px', padding: '32px', textAlign: 'center', border: '1px dashed var(--border)', borderRadius: '8px', color: 'var(--text-muted)' }}>
            No BOQ loaded. Upload a CSV or paste SKUs above to begin validation.
          </div>
        )}
        
        {boqResult && !errorMsg && (
          <div style={{ marginTop: '24px' }}>
            {(() => {
              const validationMessages = [
                ...(boqResult.fuzzy_matches || []),
                ...(boqResult.invalid_skus || []),
              ];
              return validationMessages.length > 0 ? (
                <div style={{ marginBottom: '16px' }}>
                  <h4>Validation Messages</h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '12px' }}>
                    {validationMessages.map((msg: ValidationMessage, i: number) => {
                      const bgColor = msg.severity === 'Error' ? 'rgba(239, 68, 68, 0.1)' : msg.severity === 'Warning' ? 'rgba(234, 179, 8, 0.1)' : 'rgba(59, 130, 246, 0.1)';
                      const borderColor = msg.severity === 'Error' ? '#ef4444' : msg.severity === 'Warning' ? '#eab308' : '#3b82f6';
                      return (
                        <div key={i} style={{
                          padding: '12px',
                          borderRadius: '6px',
                          background: bgColor,
                          borderLeft: `4px solid ${borderColor}`
                        }}>
                          <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>{msg.severity}</div>
                          <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>{msg.message}</div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ) : null;
            })()}
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
            
            {boqResult.rule_evaluations && boqResult.rule_evaluations.length > 0 && (() => {
              const grouped: Record<string, Record<string, any[]>> = {};
              boqResult.rule_evaluations.forEach((rule: any) => {
                const cat = rule.category || 'General';
                const subcat = rule.subcategory || 'General';
                if (!grouped[cat]) grouped[cat] = {};
                if (!grouped[cat][subcat]) grouped[cat][subcat] = [];
                grouped[cat][subcat].push(rule);
              });
              
              return (
                <div style={{ marginTop: '16px' }}>
                  <h4>Rule Evaluations</h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '12px' }}>
                    {Object.entries(grouped).map(([cat, subcats]) => (
                      <details key={cat} style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '6px', overflow: 'hidden' }}>
                        <summary style={{ padding: '12px', fontWeight: 'bold', cursor: 'pointer', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                          {cat}
                        </summary>
                        <div style={{ padding: '12px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                          {Object.entries(subcats).map(([subcat, rules]) => (
                            <details key={subcat} style={{ background: 'rgba(0,0,0,0.15)', borderRadius: '4px', overflow: 'hidden' }} open>
                              <summary style={{ padding: '8px 12px', fontWeight: '600', fontSize: '0.95rem', cursor: 'pointer', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                {subcat} <span style={{ fontSize: '0.8rem', opacity: 0.7, marginLeft: '8px' }}>({rules.length})</span>
                              </summary>
                              <div style={{ padding: '8px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                                {rules.map((rule, i: number) => (
                                  <div key={i} style={{ 
                                    padding: '12px', 
                                    borderRadius: '4px', 
                                    background: 'rgba(0,0,0,0.1)',
                                    borderLeft: `4px solid ${rule.status === 'PASS' ? '#22c55e' : '#ef4444'}`
                                  }}>
                                    <div style={{ fontWeight: 'bold', marginBottom: '4px', fontSize: '0.9rem' }}>{rule.title}</div>
                                    <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Status: {rule.status}</div>
                                    {rule.message && <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Details: {rule.message}</div>}
                                    {rule.remediations && rule.remediations.length > 0 && (
                                      <div style={{ marginTop: '8px', padding: '8px', background: 'rgba(59, 130, 246, 0.1)', borderLeft: '2px solid #3b82f6', borderRadius: '4px' }}>
                                        <div style={{ fontSize: '0.85rem', fontWeight: 'bold', color: '#3b82f6', marginBottom: '4px' }}>Suggested Fixes:</div>
                                        <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '0.85rem', color: 'var(--text-main)' }}>
                                          {rule.remediations.map((rem: string, rIdx: number) => (
                                            <li key={rIdx}>{rem}</li>
                                          ))}
                                        </ul>
                                      </div>
                                    )}
                                  </div>
                                ))}
                              </div>
                            </details>
                          ))}
                        </div>
                      </details>
                    ))}
                  </div>
                </div>
              );
            })()}
          </div>
        )}
      </div>
    </>
  );
}
