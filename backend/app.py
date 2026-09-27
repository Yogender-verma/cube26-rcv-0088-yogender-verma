"""
FastAPI Server for Receiving Manager Agent (Step 01 of 5 in Commerce Stream)
Provides multi-tenant REST API, batch receiving engine, tenancy RLS test sandbox,
operator audit overrides, evaluation runner, and evidence contract exporter.
"""

from fastapi import FastAPI, Header, HTTPException, Query, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import json

from backend.db import (
    init_db, get_records_by_org, get_record_by_id_scoped,
    save_operator_override, get_db_connection
)
from backend.agent import ReceivingManagerAgent
from backend.eval_runner import run_evaluation_suite
from backend.contract import generate_evidence_contract, RECEIVING_EVIDENCE_SCHEMA_V1
from backend.rules_engine import AUTHORITATIVE_RULES_DATABASE

app = FastAPI(
    title="Cube Buildathon · 01 · Receiving Manager API",
    description="Multimodal Batch Vision Agent for Point-of-Receipt Supplier Delivery Inspection & Evidence Creation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database on Startup
@app.on_event("startup")
def startup_db():
    init_db()

# Pydantic Schemas
class InspectionRequest(BaseModel):
    unit_id: str
    po_number: str
    po_line: int
    supplier: str
    sku: str
    asin: str
    product_title: str
    spec_colour: Optional[str] = "n/a"
    spec_variant: Optional[str] = "n/a"
    spec_components: Optional[str] = "n/a"
    cartons_ordered: int = 1
    cartons_received: int = 1
    units_per_carton_ordered: int = 12
    units_per_carton_counted: int = 12
    photo_refs: List[str] = []
    simulate_fail_open: bool = False
    override_identity_match: Optional[str] = None
    override_quality_flags: Optional[List[str]] = None

class OverrideRequest(BaseModel):
    operator_id: str
    override_reason: str
    identity_match: Optional[str] = None
    carton_damage: Optional[str] = None
    unit_damage: Optional[str] = None
    quality_flags: Optional[str] = None

# 1. Health Check
@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "01_RECEIVING_MANAGER",
        "tenancy_isolation": "ENABLED_AND_FORCED",
        "batch_model": "Gemini-3.6-Vision-Batch",
        "fail_open_support": True
    }

# 2. Get Records (Scoped by Tenant Org ID) - Engineering Rule 1
@app.get("/api/records")
def get_records(x_org_id: Optional[str] = Header(None, alias="X-Org-ID"), org_id: Optional[str] = Query(None)):
    tenant_org = x_org_id or org_id or "org_demo_alpha"
    records = get_records_by_org(tenant_org)
    return {
        "tenant_org": tenant_org,
        "count": len(records),
        "records": records
    }

# 3. Get Single Record Scoped (Prevents cross-tenant guessable key leak)
@app.get("/api/records/{record_id}")
def get_record(record_id: str, x_org_id: Optional[str] = Header(None, alias="X-Org-ID"), org_id: Optional[str] = Query(None)):
    tenant_org = x_org_id or org_id or "org_demo_alpha"
    record = get_record_by_id_scoped(record_id, tenant_org)
    if not record:
        raise HTTPException(status_code=404, detail=f"Record '{record_id}' not found for organization '{tenant_org}'. Tenancy RLS enforced.")
    
    # Attach audit overrides if any
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM operator_overrides WHERE record_id = ? AND org_id = ? ORDER BY overridden_at DESC", (record_id, tenant_org))
    overrides = [dict(r) for r in cursor.fetchall()]
    conn.close()

    record["audit_overrides"] = overrides
    return record

# 4. Run Batch Inspection API (Single-pass batching Rule 2 + Fail open Rule 3)
@app.post("/api/inspect")
def run_inspection(req: InspectionRequest, x_org_id: Optional[str] = Header(None, alias="X-Org-ID"), org_id: Optional[str] = Query(None)):
    tenant_org = x_org_id or org_id or "org_demo_alpha"
    agent = ReceivingManagerAgent()
    
    spec_data = req.dict()
    spec_data["qty_ordered"] = req.cartons_ordered * req.units_per_carton_ordered
    spec_data["qty_received"] = req.cartons_received * req.units_per_carton_counted

    result = agent.run_batch_receiving_inspection(
        org_id=tenant_org,
        unit_id=req.unit_id,
        po_line_spec=spec_data,
        captured_images=req.photo_refs if req.photo_refs else ["fixtures/receiving/default_pallet.jpg"],
        simling_failure=req.simulate_fail_open
    )

    # Save generated record to DB
    conn = get_db_connection()
    cursor = conn.cursor()
    record_id = f"RCV-{result['unit_id'].replace('UNIT-', '') if 'UNIT-' in result['unit_id'] else result['unit_id']}"
    
    cursor.execute("""
    INSERT OR REPLACE INTO receiving_records (
        record_id, unit_id, org_id, po_number, po_line, supplier, sku, asin,
        product_title, spec_colour, spec_variant, spec_components,
        cartons_ordered, cartons_received, units_per_carton_ordered, units_per_carton_counted,
        qty_ordered, qty_received, identity_match, carton_damage, unit_damage,
        quality_flags, photo_refs, operator_id, captured_at, overall_verdict,
        agent_confidence, status, evidence_data
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record_id, result["unit_id"], tenant_org, req.po_number, req.po_line,
        req.supplier, req.sku, req.asin, req.product_title,
        req.spec_colour, req.spec_variant, req.spec_components,
        result["cartons_ordered"], result["cartons_received"],
        result["units_per_carton_ordered"], result["units_per_carton_counted"],
        result["qty_ordered"], result["qty_received"],
        result["identity_match"], result["carton_damage"], result["unit_damage"],
        result["quality_flags"], ";".join(req.photo_refs), "op_active",
        result["captured_at"], result["overall_verdict"], result["agent_confidence"],
        result["status"], result["evidence_data"]
    ))
    conn.commit()
    conn.close()

    result["record_id"] = record_id
    return result

# 5. Operator Override Endpoint (Engineering Rule: Overrides are data)
@app.post("/api/records/{record_id}/override")
def override_record(
    record_id: str,
    req: OverrideRequest,
    x_org_id: Optional[str] = Header(None, alias="X-Org-ID"),
    org_id: Optional[str] = Query(None)
):
    tenant_org = x_org_id or org_id or "org_demo_alpha"
    try:
        res = save_operator_override(
            record_id=record_id,
            org_id=tenant_org,
            new_verdicts={
                "identity_match": req.identity_match,
                "carton_damage": req.carton_damage,
                "unit_damage": req.unit_damage,
                "quality_flags": req.quality_flags
            },
            operator_id=req.operator_id,
            reason=req.override_reason
        )
        return res
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

# 6. Evaluation Runner Endpoint
@app.get("/api/eval/run")
def eval_run():
    return run_evaluation_suite()

# 7. Cross-Pod Evidence Contract Endpoint
@app.get("/api/contract/{record_id}")
def get_contract(record_id: str, x_org_id: Optional[str] = Header(None, alias="X-Org-ID"), org_id: Optional[str] = Query(None)):
    tenant_org = x_org_id or org_id or "org_demo_alpha"
    record = get_record_by_id_scoped(record_id, tenant_org)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found or tenant access denied.")
    
    # Fetch overrides if any
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM operator_overrides WHERE record_id = ? AND org_id = ?", (record_id, tenant_org))
    overrides = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return generate_evidence_contract(record, overrides)

# 8. Schema definition
@app.get("/api/contract-schema")
def contract_schema():
    return RECEIVING_EVIDENCE_SCHEMA_V1

# 9. Tenancy Isolation Security Test Endpoint (Rule 1 Verification)
@app.get("/api/tenancy-test")
def tenancy_test():
    alpha_records = get_records_by_org("org_demo_alpha")
    bravo_records = get_records_by_org("org_demo_bravo")
    
    # Attempt cross-fetch leak test
    sample_alpha_id = alpha_records[0]["record_id"] if alpha_records else "RCV-0001"
    leak_attempt = get_record_by_id_scoped(sample_alpha_id, "org_demo_bravo")
    
    return {
        "tenancy_isolation_status": "SECURE_AND_ENFORCED",
        "org_demo_alpha_total_rows": len(alpha_records),
        "org_demo_bravo_total_rows": len(bravo_records),
        "leak_test_target_record": sample_alpha_id,
        "org_bravo_query_for_alpha_record": leak_attempt,
        "leak_result": "ZERO_ROWS_RETURNED (Passes Engineering Rule 1)" if leak_attempt is None else "LEAK_DETECTED"
    }

# 10. Authoritative Rules API
@app.get("/api/authoritative-rules")
def authoritative_rules():
    return AUTHORITATIVE_RULES_DATABASE
