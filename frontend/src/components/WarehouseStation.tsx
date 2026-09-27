import React, { useState } from 'react';
import { Camera, RefreshCw, AlertTriangle, CheckCircle, ShieldAlert, Layers, Box, Cpu, FileText } from 'lucide-react';
import { runInspection, InspectionPayload } from '../api';

interface Props {
  orgId: string;
  onRecordCreated: () => void;
}

export const WarehouseStation: React.FC<Props> = ({ orgId, onRecordCreated }) => {
  const [unitId, setUnitId] = useState('UNIT-0101');
  const [poNumber, setPoNumber] = useState('PO-7099');
  const [supplier, setSupplier] = useState('Supplier Coastal (DUMMY)');
  const [sku, setSku] = useState('SKU-CANDLE-3');
  const [asin, setAsin] = useState('B0DUMMY964');
  const [productTitle, setProductTitle] = useState('Soy Candle Trio');
  const [specColour, setSpecColour] = useState('cream');
  const [specVariant, setSpecVariant] = useState('3-pack');
  const [specComponents, setSpecComponents] = useState('candle x3;gift box');

  const [cartonsOrdered, setCartonsOrdered] = useState(2);
  const [cartonsReceived, setCartonsReceived] = useState(2);
  const [unitsPerCartonOrdered, setUnitsPerCartonOrdered] = useState(12);
  const [unitsPerCartonCounted, setUnitsPerCartonCounted] = useState(12);

  const [simFailOpen, setSimFailOpen] = useState(false);
  const [simDamage, setSimDamage] = useState<'none' | 'crushing' | 'water' | 'tears' | 'blur'>('none');
  const [simSpecMismatch, setSimSpecMismatch] = useState(false);

  const [loading, setLoading] = useState(false);
  const [lastResult, setLastResult] = useState<any>(null);

  const handleInspect = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setLastResult(null);

    let photoRefs = [`fixtures/receiving/${unitId}_pallet.jpg`];
    if (simDamage !== 'none') {
      photoRefs.push(`fixtures/receiving/${unitId}_carton_${simDamage}.jpg`);
    }

    const payload: InspectionPayload = {
      unit_id: unitId,
      po_number: poNumber,
      po_line: 1,
      supplier,
      sku,
      asin,
      product_title: productTitle,
      spec_colour: specColour,
      spec_variant: specVariant,
      spec_components: specComponents,
      cartons_ordered: cartonsOrdered,
      cartons_received: cartonsReceived,
      units_per_carton_ordered: unitsPerCartonOrdered,
      units_per_carton_counted: unitsPerCartonCounted,
      photo_refs: photoRefs,
      simulate_fail_open: simFailOpen,
      override_quality_flags: simSpecMismatch ? ['wrong_colour', 'missing_components'] : []
    };

    try {
      const res = await runInspection(payload, orgId);
      setLastResult(res);
      onRecordCreated();
    } catch (err: any) {
      alert('Inspection error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      {/* Left Panel: Camera & Point-of-Receipt Form */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Camera style={{ color: 'var(--accent-blue)' }} size={24} />
            <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>Point of Receipt Station</h2>
          </div>
          <span className="badge badge-pass" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Cpu size={14} /> Batch Vision Active
          </span>
        </div>

        <form onSubmit={handleInspect}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '14px' }}>
            <div>
              <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>Unit ID</label>
              <input type="text" className="form-control code-font" value={unitId} onChange={e => setUnitId(e.target.value)} required />
            </div>
            <div>
              <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>PO Number</label>
              <input type="text" className="form-control code-font" value={poNumber} onChange={e => setPoNumber(e.target.value)} required />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '14px' }}>
            <div>
              <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>SKU</label>
              <input type="text" className="form-control code-font" value={sku} onChange={e => setSku(e.target.value)} required />
            </div>
            <div>
              <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>ASIN</label>
              <input type="text" className="form-control code-font" value={asin} onChange={e => setAsin(e.target.value)} required />
            </div>
          </div>

          <div style={{ marginBottom: '14px' }}>
            <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>Product Title (PO Line)</label>
            <input type="text" className="form-control" value={productTitle} onChange={e => setProductTitle(e.target.value)} required />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '10px', marginBottom: '16px' }}>
            <div>
              <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>Spec Colour</label>
              <input type="text" className="form-control" value={specColour} onChange={e => setSpecColour(e.target.value)} />
            </div>
            <div>
              <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>Spec Variant</label>
              <input type="text" className="form-control" value={specVariant} onChange={e => setSpecVariant(e.target.value)} />
            </div>
            <div>
              <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>Spec Components</label>
              <input type="text" className="form-control" value={specComponents} onChange={e => setSpecComponents(e.target.value)} />
            </div>
          </div>

          <div style={{ background: 'rgba(0,0,0,0.3)', padding: '12px', borderRadius: '8px', marginBottom: '16px', border: '1px solid var(--border-color)' }}>
            <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--accent-cyan)', marginBottom: '10px' }}>Quantity Verification</div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: '8px' }}>
              <div>
                <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Ctns Ord</span>
                <input type="number" className="form-control" value={cartonsOrdered} onChange={e => setCartonsOrdered(Number(e.target.value))} />
              </div>
              <div>
                <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Ctns Rec</span>
                <input type="number" className="form-control" value={cartonsReceived} onChange={e => setCartonsReceived(Number(e.target.value))} />
              </div>
              <div>
                <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Units/Ctn (Ord)</span>
                <input type="number" className="form-control" value={unitsPerCartonOrdered} onChange={e => setUnitsPerCartonOrdered(Number(e.target.value))} />
              </div>
              <div>
                <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Units/Ctn (Cnt)</span>
                <input type="number" className="form-control" value={unitsPerCartonCounted} onChange={e => setUnitsPerCartonCounted(Number(e.target.value))} />
              </div>
            </div>
          </div>

          <div style={{ background: 'rgba(0,0,0,0.2)', padding: '12px', borderRadius: '8px', marginBottom: '20px', border: '1px dashed var(--border-color)' }}>
            <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-secondary)', marginBottom: '8px' }}>Simulation Controls (Rule Verification)</div>
            <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', fontSize: '0.8rem' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer' }}>
                <input type="checkbox" checked={simFailOpen} onChange={e => setSimFailOpen(e.target.checked)} />
                <span>Simulate Pipeline Timeout (Rule 3 - Fail Open)</span>
              </label>

              <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer' }}>
                <input type="checkbox" checked={simSpecMismatch} onChange={e => setSimSpecMismatch(e.target.checked)} />
                <span>Simulate Quality Spec Mismatch</span>
              </label>

              <div style={{ width: '100%', display: 'flex', alignItems: 'center', gap: '10px', marginTop: '4px' }}>
                <span style={{ color: 'var(--text-muted)' }}>Visual Damage:</span>
                {(['none', 'crushing', 'water', 'tears', 'blur'] as const).map(d => (
                  <button
                    key={d}
                    type="button"
                    className={`btn ${simDamage === d ? 'btn-primary' : 'btn-secondary'}`}
                    style={{ padding: '2px 8px', fontSize: '0.75rem' }}
                    onClick={() => setSimDamage(d)}
                  >
                    {d}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <button type="submit" className="btn btn-primary" style={{ width: '100%', padding: '12px' }} disabled={loading}>
            {loading ? <RefreshCw className="pulse-active" size={18} /> : <Camera size={18} />}
            {loading ? 'Processing Single-Pass Batch Inspection...' : 'Capture & Execute Batch Agent Inspection'}
          </button>
        </form>
      </div>

      {/* Right Panel: Bounding Box & Agent Verdict Output */}
      <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Box style={{ color: 'var(--accent-purple)' }} size={24} />
          Live Computer Vision & Decision Proof
        </h2>

        {/* Photorealistic Camera Simulator with Overlay */}
        <div style={{
          position: 'relative',
          height: '240px',
          background: 'linear-gradient(135deg, #0d131f, #1e293b)',
          borderRadius: '10px',
          border: '1px solid var(--border-color)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          overflow: 'hidden',
          marginBottom: '20px'
        }}>
          {/* Simulated Palette Box Grid */}
          <div style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
            <Layers size={48} style={{ opacity: 0.3, marginBottom: '8px' }} />
            <div style={{ fontSize: '0.85rem' }}>Camera Stream Feed · Point of Receipt</div>
            <div className="code-font" style={{ fontSize: '0.75rem', color: 'var(--accent-cyan)' }}>{unitId} - {sku}</div>
          </div>

          {/* Bounding Box Visual Overlay */}
          {lastResult && lastResult.overall_verdict !== 'PENDING_REVIEW' && (
            <div style={{
              position: 'absolute',
              top: '20px',
              left: '30px',
              right: '30px',
              bottom: '20px',
              border: `2px dashed ${lastResult.overall_verdict === 'PASS' ? '#10b981' : (lastResult.overall_verdict === 'FAIL' ? '#f43f5e' : '#f59e0b')}`,
              borderRadius: '8px',
              background: 'rgba(0,0,0,0.25)',
              padding: '10px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className={`badge ${lastResult.overall_verdict === 'PASS' ? 'badge-pass' : (lastResult.overall_verdict === 'FAIL' ? 'badge-fail' : 'badge-uncertain')}`}>
                  {lastResult.overall_verdict} ({Math.round(lastResult.agent_confidence * 100)}% Conf)
                </span>
                <span className="code-font" style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Single-Pass Batch {lastResult.batch_execution_time_ms}ms</span>
              </div>
              <div style={{ fontSize: '0.75rem', color: 'white', background: 'rgba(0,0,0,0.6)', padding: '6px 10px', borderRadius: '4px' }}>
                Detection: Identity={lastResult.identity_match} | Carton={lastResult.carton_damage} | Unit={lastResult.unit_damage}
              </div>
            </div>
          )}
        </div>

        {/* Decision Breakdown */}
        {lastResult ? (
          <div style={{ flex: 1, background: 'rgba(0,0,0,0.3)', padding: '16px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <div style={{ fontSize: '0.9rem', fontWeight: 700 }}>Record Created: {lastResult.record_id}</div>
              <span className={`badge ${lastResult.overall_verdict === 'PASS' ? 'badge-pass' : (lastResult.overall_verdict === 'FAIL' ? 'badge-fail' : (lastResult.overall_verdict === 'PENDING_REVIEW' ? 'badge-pending' : 'badge-uncertain'))}`}>
                {lastResult.overall_verdict}
              </span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '0.8rem', marginBottom: '12px' }}>
              <div><span style={{ color: 'var(--text-muted)' }}>Identity Match:</span> <strong>{lastResult.identity_match}</strong></div>
              <div><span style={{ color: 'var(--text-muted)' }}>Carton Damage:</span> <strong>{lastResult.carton_damage}</strong></div>
              <div><span style={{ color: 'var(--text-muted)' }}>Qty Count:</span> <strong>{lastResult.qty_received} / {lastResult.qty_ordered}</strong></div>
              <div><span style={{ color: 'var(--text-muted)' }}>Quality Flags:</span> <strong>{lastResult.quality_flags || 'None'}</strong></div>
            </div>

            {lastResult.overall_verdict === 'PENDING_REVIEW' && (
              <div style={{ background: 'rgba(139, 92, 246, 0.2)', color: '#c084fc', padding: '10px', borderRadius: '6px', fontSize: '0.8rem', display: 'flex', gap: '8px', alignItems: 'center' }}>
                <ShieldAlert size={18} />
                <span>Fail-Open Safeguard Triggered: Saved to DB as Pending Review. Operations line not blocked.</span>
              </div>
            )}
          </div>
        ) : (
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            Ready for shipment inspection. Click 'Capture & Execute Batch Agent Inspection' to run.
          </div>
        )}
      </div>
    </div>
  );
};
