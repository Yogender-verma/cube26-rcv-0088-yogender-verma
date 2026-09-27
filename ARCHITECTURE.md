# ARCHITECTURE.md · Receiving Manager Agent

**Participant:** Yogender Verma  
**Repository:** `cube26-rcv-0088-yogender-verma`  
**Problem Statement:** 01 · Receiving Manager (Step 1 of 5 in Commerce Context Stream)

---

## 1. High-Level Architectural Diagram

```text
  Physical Pallet Arrival at Warehouse Dock
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  Point-of-Receipt Station (React + Vite Dashboard UI)    │
│  - Live Camera / Barcode Stream                         │
│  - PO Line Lookup & Spec Selector                        │
│  - Bounding Box Bounding Overlay                         │
│  - Real-Time Verdict Visualizer                          │
└────────────────────────────┬─────────────────────────────┘
                             │
                             │ REST API (X-Org-ID Header)
                             ▼
┌──────────────────────────────────────────────────────────┐
│  FastAPI Backend (Tenancy Isolation Enforcement Middleware)│
│  - Row-Level Security (RLS) Scoped Queries               │
│  - Fail-Open Exception & Latency Circuit Breaker         │
└────────────────────────────┬─────────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│ ReceivingManagerAgent   │       │ Authoritative Rules Engine│
│ - Single-Pass Batch Call│       │ - Amazon FBA Inbound Spec│
│ - 5 Inspection Checks   │       │ - 3PL Inbound SOPs      │
│ - Uncertainty Scoring   │       └────────────┬────────────┘
└───────────┬─────────────┘                    │
            │                                  │
            └────────────────┬─────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│  SQLite Database + Immutable Audit Ledger                 │
│  - receiving_records (Scoped by org_id)                  │
│  - operator_overrides (Honesty Rule: Overrides are data)  │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│  Cross-Pod Evidence Contract JSON Exporter               │
│  (Consumed by Step 02 Prep Manager & Step 05 Recovery)  │
└──────────────────────────────────────────────────────────┘
```

---

## 2. Component Breakdown

### A. Point-of-Receipt Station (`frontend/`)
- Built with React 18, Vite, TypeScript, and custom CSS design tokens.
- Displays live camera feeds, bounding box detections, and real-time PASS/FAIL/UNCERTAIN badges.
- Features multi-tenant switcher (`org_demo_alpha` vs `org_demo_bravo`) for immediate security verification.

### B. Single-Pass Batch Vision Engine (`backend/agent.py`)
- **Engineering Rule 2 Compliance**: Makes a single pass per unit carrying all 5 checks:
  1. Identity Match against PO line
  2. Quantity Verification (Cartons received × Units counted)
  3. Carton Damage Inspection (Crushing, Water, Tears)
  4. Unit Damage Inspection
  5. Quality Flags against agreed Spec (Color, Variant, Components)
- **Engineering Rule 3 Compliance (Fail Open)**: Any network latency spike or model exception catches cleanly and saves the capture as `PENDING_REVIEW`, allowing dock operators to proceed uninterrupted.
- **Engineering Rule 4 Compliance (Uncertain Verdict)**: Images with lighting glare or resolution under threshold output `UNCERTAIN` rather than guessing a false PASS/FAIL.

### C. Multi-Tenancy & Row-Level Security (`backend/db.py`)
- **Engineering Rule 1 Compliance**: Every SQL statement enforces `WHERE org_id = ?`. Queries executed under `org_demo_bravo` return ZERO rows of `org_demo_alpha`.

### D. Authoritative Channel Rules Engine (`backend/rules_engine.py`)
- **Engineering Rule 5 Compliance**: References official Amazon FBA and 3PL inbound policies rather than relying on memory or dummy CSV flags.

### E. Audit Override Ledger (`backend/db.py`)
- **Honesty Rule Compliance**: When dock supervisors override an automated verdict, both original and modified verdicts are recorded with operator ID, timestamp, and mandatory justification reason.

---

## 3. Data Contract Specification

Conforms to standard Cross-Pod Evidence Schema Version 1.0.0.
Output JSON schema stored in [`submissions/yogender-verma/contract/receiving_evidence_schema.json`](submissions/yogender-verma/contract/receiving_evidence_schema.json).
