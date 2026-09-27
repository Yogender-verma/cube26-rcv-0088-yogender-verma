import React, { useState } from 'react';
import { ReceivingRecord } from '../api';
import { Search, Eye, Edit3, ShieldAlert, CheckCircle, AlertTriangle, FileText } from 'lucide-react';

interface Props {
  records: ReceivingRecord[];
  onSelectRecord: (rec: ReceivingRecord) => void;
  onOpenOverride: (rec: ReceivingRecord) => void;
  onViewContract: (rec: ReceivingRecord) => void;
}

export const HistoryTable: React.FC<Props> = ({ records, onSelectRecord, onOpenOverride, onViewContract }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [verdictFilter, setVerdictFilter] = useState('ALL');

  const filtered = records.filter(r => {
    const matchSearch = r.record_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                        r.unit_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                        r.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
                        r.supplier.toLowerCase().includes(searchTerm.toLowerCase()) ||
                        r.po_number.toLowerCase().includes(searchTerm.toLowerCase());
    const matchVerdict = verdictFilter === 'ALL' || r.overall_verdict === verdictFilter;
    return matchSearch && matchVerdict;
  });

  return (
    <div className="glass-panel" style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>Receiving Inspection Audit History</h2>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            Scoped Row-Level Security (Tenant Isolation Active) · Total: {filtered.length} records
          </div>
        </div>

        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          {/* Verdict Filters */}
          <div style={{ display: 'flex', background: 'var(--bg-tertiary)', padding: '3px', borderRadius: '6px' }}>
            {['ALL', 'PASS', 'FAIL', 'UNCERTAIN', 'PENDING_REVIEW'].map(v => (
              <button
                key={v}
                onClick={() => setVerdictFilter(v)}
                style={{
                  background: verdictFilter === v ? 'var(--accent-blue)' : 'transparent',
                  color: verdictFilter === v ? 'white' : 'var(--text-muted)',
                  border: 'none',
                  padding: '4px 10px',
                  borderRadius: '4px',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                {v}
              </button>
            ))}
          </div>

          {/* Search Bar */}
          <div style={{ position: 'relative', width: '220px' }}>
            <Search size={16} style={{ position: 'absolute', left: '10px', top: '10px', color: 'var(--text-muted)' }} />
            <input
              type="text"
              className="form-control"
              placeholder="Search Record, Unit, SKU..."
              style={{ paddingLeft: '32px' }}
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
      </div>

      {/* Table */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)' }}>
              <th style={{ padding: '10px' }}>Record ID</th>
              <th style={{ padding: '10px' }}>Unit ID</th>
              <th style={{ padding: '10px' }}>PO / Supplier</th>
              <th style={{ padding: '10px' }}>SKU & Spec</th>
              <th style={{ padding: '10px' }}>Qty (Rec/Ord)</th>
              <th style={{ padding: '10px' }}>Damage</th>
              <th style={{ padding: '10px' }}>Quality Flags</th>
              <th style={{ padding: '10px' }}>Overall Verdict</th>
              <th style={{ padding: '10px', textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(r => (
              <tr key={r.record_id} style={{ borderBottom: '1px solid var(--border-color)', transition: 'background 0.15s' }}>
                <td style={{ padding: '10px', fontWeight: 600 }} className="code-font">{r.record_id}</td>
                <td style={{ padding: '10px' }} className="code-font">{r.unit_id}</td>
                <td style={{ padding: '10px' }}>
                  <div>{r.po_number}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{r.supplier}</div>
                </td>
                <td style={{ padding: '10px' }}>
                  <div className="code-font">{r.sku}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{r.spec_colour} | {r.spec_variant}</div>
                </td>
                <td style={{ padding: '10px' }}>
                  <span style={{ color: r.qty_received !== r.qty_ordered ? 'var(--accent-rose)' : 'inherit', fontWeight: 600 }}>
                    {r.qty_received} / {r.qty_ordered}
                  </span>
                </td>
                <td style={{ padding: '10px' }}>
                  <div style={{ fontSize: '0.75rem' }}>Ctn: <strong style={{ color: r.carton_damage !== 'none' ? 'var(--accent-amber)' : 'inherit' }}>{r.carton_damage}</strong></div>
                  <div style={{ fontSize: '0.75rem' }}>Unit: <strong style={{ color: r.unit_damage !== 'none' ? 'var(--accent-amber)' : 'inherit' }}>{r.unit_damage}</strong></div>
                </td>
                <td style={{ padding: '10px' }}>
                  {r.quality_flags ? (
                    <span style={{ background: 'rgba(244,63,94,0.15)', color: '#fb7185', padding: '2px 6px', borderRadius: '4px', fontSize: '0.7rem' }}>
                      {r.quality_flags}
                    </span>
                  ) : (
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>—</span>
                  )}
                </td>
                <td style={{ padding: '10px' }}>
                  <span className={`badge ${r.overall_verdict === 'PASS' ? 'badge-pass' : (r.overall_verdict === 'FAIL' ? 'badge-fail' : (r.overall_verdict === 'PENDING_REVIEW' ? 'badge-pending' : 'badge-uncertain'))}`}>
                    {r.overall_verdict}
                  </span>
                </td>
                <td style={{ padding: '10px', textAlign: 'right' }}>
                  <div style={{ display: 'flex', gap: '6px', justifyContent: 'flex-end' }}>
                    <button className="btn btn-secondary" style={{ padding: '4px 8px', fontSize: '0.75rem' }} onClick={() => onSelectRecord(r)} title="Evidence Deep-Dive">
                      <Eye size={14} /> Evidence
                    </button>
                    <button className="btn btn-secondary" style={{ padding: '4px 8px', fontSize: '0.75rem' }} onClick={() => onOpenOverride(r)} title="Log Operator Override">
                      <Edit3 size={14} /> Override
                    </button>
                    <button className="btn btn-secondary" style={{ padding: '4px 8px', fontSize: '0.75rem' }} onClick={() => onViewContract(r)} title="Cross-Pod Contract JSON">
                      <FileText size={14} /> JSON
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
