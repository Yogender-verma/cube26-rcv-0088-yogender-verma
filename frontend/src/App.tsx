import React, { useState, useEffect } from 'react';
import { WarehouseStation } from './components/WarehouseStation';
import { HistoryTable } from './components/HistoryTable';
import { EvidenceModal } from './components/EvidenceModal';
import { OverrideModal } from './components/OverrideModal';
import { EvalDashboard } from './components/EvalDashboard';
import { TenancySandbox } from './components/TenancySandbox';
import { ContractViewer } from './components/ContractViewer';
import { DeliverablesHub } from './components/DeliverablesHub';
import { fetchRecords, retryInspection, ReceivingRecord } from './api';
import { Box, Camera, History, BarChart3, Lock, FileText, BookOpen, Layers, Cpu, ShieldCheck } from 'lucide-react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'station' | 'history' | 'eval' | 'tenancy' | 'contract' | 'docs'>('station');
  const [orgId, setOrgId] = useState('org_demo_alpha');
  const [records, setRecords] = useState<ReceivingRecord[]>([]);

  const [selectedRecord, setSelectedRecord] = useState<ReceivingRecord | null>(null);
  const [overrideRecord, setOverrideRecord] = useState<ReceivingRecord | null>(null);

  const loadData = async () => {
    try {
      const recs = await fetchRecords(orgId);
      setRecords(recs);
    } catch (err: any) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadData();
  }, [orgId]);

  return (
    <div style={{ padding: '24px', maxWidth: '1440px', margin: '0 auto' }}>
      {/* Top Header Bar */}
      <header className="glass-panel" style={{ padding: '16px 24px', marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)', width: '42px', height: '42px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Box size={24} style={{ color: 'white' }} />
          </div>
          <div>
            <h1 style={{ fontSize: '1.35rem', fontWeight: 800, background: 'linear-gradient(135deg, #f8fafc, #94a3b8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Cube Buildathon · 01 · Receiving Manager
            </h1>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Point-of-Receipt Visual Inspection & Evidence Engine · Step 01 of 5
            </div>
          </div>
        </div>

        {/* Controls & Tenant Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'var(--bg-tertiary)', padding: '6px 12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <Lock size={16} style={{ color: 'var(--accent-purple)' }} />
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Active Tenant:</span>
            <select
              value={orgId}
              onChange={e => setOrgId(e.target.value)}
              className="code-font"
              style={{ background: 'transparent', color: 'var(--text-primary)', border: 'none', fontWeight: 700, cursor: 'pointer', outline: 'none' }}
            >
              <option value="org_demo_alpha" style={{ background: '#121824' }}>org_demo_alpha</option>
              <option value="org_demo_bravo" style={{ background: '#121824' }}>org_demo_bravo</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span className="badge badge-pass" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Cpu size={14} /> Gemini 3.6 Vision
            </span>
            <span className="badge badge-pass" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <ShieldCheck size={14} /> RLS Forced
            </span>
          </div>
        </div>
      </header>

      {/* Main Tab Navigation */}
      <nav style={{ display: 'flex', gap: '10px', marginBottom: '24px' }}>
        {[
          { id: 'station', label: 'Warehouse Dock Station', icon: Camera },
          { id: 'history', label: `Receiving Records (${records.length})`, icon: History },
          { id: 'eval', label: 'Evaluation & Failure Modes', icon: BarChart3 },
          { id: 'tenancy', label: 'Tenancy Security Sandbox', icon: Lock },
          { id: 'contract', label: 'Cross-Pod JSON Contract', icon: FileText },
          { id: 'docs', label: 'Submission Deliverables', icon: BookOpen }
        ].map(tab => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              className={`btn ${isActive ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '10px 18px', fontSize: '0.85rem' }}
              onClick={() => setActiveTab(tab.id as any)}
            >
              <Icon size={16} />
              {tab.label}
            </button>
          );
        })}
      </nav>

      {/* Main Tab Content */}
      <main>
        {activeTab === 'station' && <WarehouseStation orgId={orgId} onRecordCreated={loadData} />}
        {activeTab === 'history' && (
          <HistoryTable
            records={records}
            onSelectRecord={r => setSelectedRecord(r)}
            onOpenOverride={r => setOverrideRecord(r)}
            onViewContract={r => { setSelectedRecord(r); setActiveTab('contract'); }}
            onRetryRecord={async r => {
              try {
                await retryInspection(r.record_id, orgId);
                await loadData();
                alert(`Inspection retry complete for record ${r.record_id}!`);
              } catch (err: any) {
                alert(`Retry failed: ${err.message}`);
              }
            }}
          />
        )}
        {activeTab === 'eval' && <EvalDashboard />}
        {activeTab === 'tenancy' && <TenancySandbox />}
        {activeTab === 'contract' && <ContractViewer selectedRecord={selectedRecord || records[0]} orgId={orgId} />}
        {activeTab === 'docs' && <DeliverablesHub />}
      </main>

      {/* Modals */}
      <EvidenceModal record={selectedRecord} onClose={() => setSelectedRecord(null)} />
      <OverrideModal record={overrideRecord} orgId={orgId} onClose={() => setOverrideRecord(null)} onSaved={loadData} />
    </div>
  );
};
