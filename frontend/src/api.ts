export interface ReceivingRecord {
  record_id: string;
  unit_id: string;
  org_id: string;
  po_number: string;
  po_line: number;
  supplier: string;
  sku: string;
  asin: string;
  product_title: string;
  spec_colour?: string;
  spec_variant?: string;
  spec_components?: string;
  cartons_ordered: number;
  cartons_received: number;
  units_per_carton_ordered: number;
  units_per_carton_counted: number;
  qty_ordered: number;
  qty_received: number;
  identity_match: string;
  carton_damage: string;
  unit_damage: string;
  quality_flags: string;
  photo_refs: string;
  operator_id: string;
  captured_at: string;
  overall_verdict: string;
  agent_confidence: number;
  status: string;
  evidence_data?: string;
  audit_overrides?: any[];
}

export interface InspectionPayload {
  unit_id: string;
  po_number: string;
  po_line: number;
  supplier: string;
  sku: string;
  asin: string;
  product_title: string;
  spec_colour?: string;
  spec_variant?: string;
  spec_components?: string;
  cartons_ordered: number;
  cartons_received: number;
  units_per_carton_ordered: number;
  units_per_carton_counted: number;
  photo_refs?: string[];
  simulate_fail_open?: boolean;
  override_identity_match?: string;
  override_quality_flags?: string[];
}

const API_BASE = 'http://localhost:8000/api';

export async function fetchRecords(orgId: string): Promise<ReceivingRecord[]> {
  const res = await fetch(`${API_BASE}/records`, {
    headers: { 'X-Org-ID': orgId }
  });
  if (!res.ok) throw new Error('Failed to fetch records');
  const data = await res.json();
  return data.records;
}

export async function fetchRecordById(recordId: string, orgId: string): Promise<ReceivingRecord> {
  const res = await fetch(`${API_BASE}/records/${recordId}`, {
    headers: { 'X-Org-ID': orgId }
  });
  if (!res.ok) throw new Error('Failed to fetch record or access denied by tenant RLS');
  return res.json();
}

export async function runInspection(payload: InspectionPayload, orgId: string) {
  const res = await fetch(`${API_BASE}/inspect`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Org-ID': orgId
    },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Inspection execution failed');
  return res.json();
}

export async function submitOverride(recordId: string, orgId: string, override: {
  operator_id: string;
  override_reason: string;
  identity_match?: string;
  carton_damage?: string;
  unit_damage?: string;
  quality_flags?: string;
}) {
  const res = await fetch(`${API_BASE}/records/${recordId}/override`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Org-ID': orgId
    },
    body: JSON.stringify(override)
  });
  if (!res.ok) throw new Error('Failed to submit operator override');
  return res.json();
}

export async function runEvalSuite() {
  const res = await fetch(`${API_BASE}/eval/run`);
  if (!res.ok) throw new Error('Failed to run evaluation suite');
  return res.json();
}

export async function fetchTenancyTest() {
  const res = await fetch(`${API_BASE}/tenancy-test`);
  if (!res.ok) throw new Error('Failed to run tenancy test');
  return res.json();
}

export async function fetchContract(recordId: string, orgId: string) {
  const res = await fetch(`${API_BASE}/contract/${recordId}`, {
    headers: { 'X-Org-ID': orgId }
  });
  if (!res.ok) throw new Error('Failed to fetch evidence contract');
  return res.json();
}

export async function fetchAuthoritativeRules() {
  const res = await fetch(`${API_BASE}/authoritative-rules`);
  if (!res.ok) throw new Error('Failed to fetch authoritative rules');
  return res.json();
}
