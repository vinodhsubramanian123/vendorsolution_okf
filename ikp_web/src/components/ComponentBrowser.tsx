import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const CATEGORY_COLORS: Record<string, string> = {
  CPU: '#6366f1',
  Memory: '#0ea5e9',
  Storage: '#f59e0b',
  GPU: '#a855f7',
  Networking: '#10b981',
  NIC: '#14b8a6',
  PSU: '#f97316',
  Infrastructure: '#64748b',
  Accessory: '#94a3b8',
  Security: '#ef4444',
  Uncategorized: '#475569',
};

function categoryColor(cat: string) {
  return CATEGORY_COLORS[cat] || '#6366f1';
}

interface ComponentItem {
  id: string;
  title: string;
  description?: string;
  category?: string;
  subcategory?: string;
  platform_id?: string;
  part_number?: string;
  confidence?: string;
  lifecycle_status?: string;
  type?: string;
}

interface BomData {
  platform_id: string;
  platform_title: string;
  category_count: number;
  total_components: number;
  bom: Record<string, ComponentItem[]>;
}

const PLATFORMS = [
  { id: 'hpe-proliant-dl380-gen12', label: 'HPE ProLiant DL380 Gen12' },
  { id: 'hpe-proliant-dl580-gen12', label: 'HPE ProLiant DL580 Gen12' },
  { id: 'hpe-alletra-storage-mp-b10000', label: 'HPE Alletra MP B10000' },
];

export function ComponentBrowser() {
  const [selectedPlatform, setSelectedPlatform] = useState(PLATFORMS[0].id);
  const [bomData, setBomData] = useState<BomData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedCats, setExpandedCats] = useState<Set<string>>(new Set());
  const [searchFilter, setSearchFilter] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedComponent, setSelectedComponent] = useState<ComponentItem | null>(null);

  const fetchBom = useCallback(async (platformId: string) => {
    setLoading(true);
    setError(null);
    setBomData(null);
    setSelectedCategory(null);
    setSelectedComponent(null);
    try {
      const res = await axios.get(`${API_BASE}/platforms/${platformId}/bom`);
      setBomData(res.data);
      // Auto-expand all categories
      setExpandedCats(new Set(Object.keys(res.data.bom)));
    } catch (e: any) {
      setError(e.response?.data?.detail || e.message || 'Failed to load BOM');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchBom(selectedPlatform);
  }, [selectedPlatform, fetchBom]);

  const toggleCat = (cat: string) => {
    setExpandedCats(prev => {
      const next = new Set(prev);
      if (next.has(cat)) next.delete(cat);
      else next.add(cat);
      return next;
    });
  };

  const filteredBom = bomData
    ? Object.entries(bomData.bom).filter(([cat]) =>
        !selectedCategory || cat === selectedCategory
      ).map(([cat, items]) => [
        cat,
        items.filter(item =>
          !searchFilter ||
          (item.title || '').toLowerCase().includes(searchFilter.toLowerCase()) ||
          (item.description || '').toLowerCase().includes(searchFilter.toLowerCase()) ||
          (item.part_number || '').toLowerCase().includes(searchFilter.toLowerCase())
        ),
      ] as [string, ComponentItem[]])
    : [];

  const confidenceBadge = (conf?: string) => {
    const color = conf === 'High' ? '#22c55e' : conf === 'Medium' ? '#f59e0b' : '#64748b';
    return (
      <span style={{
        fontSize: '0.7rem', padding: '1px 6px', borderRadius: '10px',
        background: `${color}22`, color, border: `1px solid ${color}55`,
        marginLeft: '6px', fontWeight: 600,
      }}>
        {conf || 'Unverified'}
      </span>
    );
  };

  return (
    <div style={{ display: 'flex', height: '100%', gap: '16px', padding: '16px' }}>
      {/* Left Panel: Controls + Category Nav */}
      <div style={{ width: '240px', flexShrink: 0, display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div>
          <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>
            Platform
          </label>
          <select
            value={selectedPlatform}
            onChange={e => setSelectedPlatform(e.target.value)}
            style={{
              width: '100%', padding: '8px', borderRadius: '6px',
              background: 'var(--surface)', border: '1px solid var(--border)',
              color: 'var(--text-main)', fontSize: '0.85rem',
            }}
          >
            {PLATFORMS.map(p => (
              <option key={p.id} value={p.id}>{p.label}</option>
            ))}
          </select>
        </div>

        <div>
          <input
            type="text"
            placeholder="Filter components..."
            value={searchFilter}
            onChange={e => setSearchFilter(e.target.value)}
            style={{
              width: '100%', padding: '8px', borderRadius: '6px', boxSizing: 'border-box',
              background: 'var(--surface)', border: '1px solid var(--border)',
              color: 'var(--text-main)', fontSize: '0.85rem',
            }}
          />
        </div>

        {bomData && (
          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '8px' }}>
              {bomData.total_components} components across {bomData.category_count} categories
            </div>
            <button
              onClick={() => setSelectedCategory(null)}
              style={{
                width: '100%', textAlign: 'left', padding: '6px 10px',
                borderRadius: '6px', border: 'none', cursor: 'pointer', marginBottom: '4px',
                background: !selectedCategory ? 'rgba(99,102,241,0.2)' : 'transparent',
                color: !selectedCategory ? '#818cf8' : 'var(--text-muted)',
                fontWeight: !selectedCategory ? 700 : 400, fontSize: '0.85rem',
              }}
            >
              All Categories
            </button>
            {Object.entries(bomData.bom).map(([cat, items]) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(selectedCategory === cat ? null : cat)}
                style={{
                  width: '100%', textAlign: 'left', padding: '6px 10px',
                  borderRadius: '6px', border: 'none', cursor: 'pointer', marginBottom: '2px',
                  background: selectedCategory === cat ? `${categoryColor(cat)}22` : 'transparent',
                  color: selectedCategory === cat ? categoryColor(cat) : 'var(--text-muted)',
                  fontWeight: selectedCategory === cat ? 700 : 400, fontSize: '0.85rem',
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                }}
              >
                <span>⬡ {cat}</span>
                <span style={{
                  fontSize: '0.7rem', padding: '1px 6px', borderRadius: '10px',
                  background: 'rgba(255,255,255,0.1)',
                }}>
                  {items.length}
                </span>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Center Panel: Component List */}
      <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {loading && (
          <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
            Loading bill of materials...
          </div>
        )}
        {error && (
          <div style={{ padding: '16px', borderRadius: '8px', background: '#fee2e2', color: '#991b1b' }}>
            {error}
          </div>
        )}
        {!loading && !error && filteredBom.map(([cat, items]) => (
          items.length === 0 ? null : (
            <div key={cat} style={{ borderRadius: '8px', overflow: 'hidden', border: '1px solid var(--border)' }}>
              <div
                onClick={() => toggleCat(cat)}
                style={{
                  padding: '10px 14px', cursor: 'pointer', display: 'flex',
                  justifyContent: 'space-between', alignItems: 'center',
                  background: `${categoryColor(cat)}15`,
                  borderLeft: `4px solid ${categoryColor(cat)}`,
                }}
              >
                <span style={{ fontWeight: 700, color: categoryColor(cat) }}>
                  {expandedCats.has(cat) ? '▾' : '▸'} {cat}
                </span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  {items.length} items
                </span>
              </div>

              {expandedCats.has(cat) && (
                <div>
                  {/* Group by subcategory */}
                  {(() => {
                    const subcats: Record<string, ComponentItem[]> = {};
                    items.forEach(item => {
                      const sc = item.subcategory || 'General';
                      if (!subcats[sc]) subcats[sc] = [];
                      subcats[sc].push(item);
                    });
                    return Object.entries(subcats).map(([sc, scItems]) => (
                      <div key={sc}>
                        {Object.keys(subcats).length > 1 && (
                          <div style={{
                            padding: '4px 14px', fontSize: '0.75rem', fontWeight: 600,
                            color: 'var(--text-muted)', background: 'rgba(0,0,0,0.1)',
                            borderTop: '1px solid var(--border)',
                          }}>
                            {sc}
                          </div>
                        )}
                        {scItems.map(item => (
                          <div
                            key={item.id}
                            onClick={() => setSelectedComponent(item)}
                            style={{
                              padding: '10px 14px', cursor: 'pointer',
                              borderTop: '1px solid var(--border)',
                              background: selectedComponent?.id === item.id
                                ? 'rgba(99,102,241,0.12)' : 'transparent',
                              transition: 'background 0.15s',
                            }}
                            onMouseEnter={e => {
                              if (selectedComponent?.id !== item.id)
                                (e.currentTarget as HTMLElement).style.background = 'rgba(255,255,255,0.04)';
                            }}
                            onMouseLeave={e => {
                              if (selectedComponent?.id !== item.id)
                                (e.currentTarget as HTMLElement).style.background = 'transparent';
                            }}
                          >
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                              <div style={{ flex: 1, minWidth: 0 }}>
                                <div style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-main)' }}>
                                  {item.title || item.id}
                                  {confidenceBadge(item.confidence)}
                                </div>
                                {item.part_number && (
                                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                                    Part #: <code style={{ color: '#94a3b8' }}>{item.part_number}</code>
                                  </div>
                                )}
                              </div>
                              <span style={{
                                fontSize: '0.7rem', color: 'var(--text-muted)',
                                background: 'rgba(255,255,255,0.06)', padding: '2px 6px',
                                borderRadius: '4px', marginLeft: '8px', flexShrink: 0,
                              }}>
                                {item.type}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    ));
                  })()}
                </div>
              )}
            </div>
          )
        ))}
      </div>

      {/* Right Panel: Component Detail */}
      {selectedComponent && (
        <div style={{
          width: '300px', flexShrink: 0, borderRadius: '8px', border: '1px solid var(--border)',
          padding: '16px', background: 'var(--surface)', overflowY: 'auto',
          display: 'flex', flexDirection: 'column', gap: '12px',
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <h3 style={{ margin: 0, fontSize: '1rem', color: 'var(--text-main)' }}>
              Component Detail
            </h3>
            <button
              onClick={() => setSelectedComponent(null)}
              style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', fontSize: '1.2rem' }}
            >
              ×
            </button>
          </div>

          <div style={{ borderLeft: `3px solid ${categoryColor(selectedComponent.category || '')}`, paddingLeft: '10px' }}>
            <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>{selectedComponent.title}</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>
              {selectedComponent.id}
            </div>
          </div>

          {selectedComponent.description && (
            <div>
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>DESCRIPTION</div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-main)', lineHeight: 1.5 }}>
                {selectedComponent.description}
              </div>
            </div>
          )}

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
            {[
              ['Category', selectedComponent.category],
              ['Subcategory', selectedComponent.subcategory],
              ['Part Number', selectedComponent.part_number],
              ['Confidence', selectedComponent.confidence],
              ['Lifecycle', selectedComponent.lifecycle_status],
              ['Type', selectedComponent.type],
            ].filter(([, v]) => v).map(([label, value]) => (
              <div key={label as string} style={{ padding: '8px', borderRadius: '6px', background: 'rgba(0,0,0,0.2)' }}>
                <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase' }}>
                  {label}
                </div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-main)', marginTop: '2px' }}>
                  {value}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
