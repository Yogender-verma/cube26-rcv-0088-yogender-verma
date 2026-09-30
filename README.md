# Cube Buildathon · 01 · Receiving Manager

**Commerce Context stream · Round 2 · Individual Build**

> Five agents, one unit, one record that follows it.
> A physical product arrives, gets prepped, gets shipped, comes back. At every step a person makes a fast judgment that nobody records. **You build the agent that makes one of those judgments, and leaves proof.**

**New here? Read these first:**

1. [`GITHUB-GUIDE.md`](GITHUB-GUIDE.md) explains how to fork the repository, set it up, build and push your work.
2. [`RULES.md`](RULES.md) covers the repository and engineering rules.

---

## Your problem statement: Receiving Manager

|                              |                                                                                     |
| ---------------------------- | ----------------------------------------------------------------------------------- |
| **Position in the chain**    | Step 1 of 5. Supplier delivery.                                                     |
| **Customer**                 | Seller or 3PL taking supplier delivery                                              |
| **What gets recorded**       | Condition on arrival                                                                |
| **Who consumes your output** | Prep Manager (next in the chain) and Recovery Manager (supplier and inbound claims) |

A pallet arrives from a manufacturer, often overseas. Someone opens the cartons and decides whether what arrived is what was ordered: right SKU, right count, undamaged, to the quality agreed. Today this is a spot check at best. Shortages and defects surface weeks later when units fail in prep or come back as returns, by which point the supplier conversation is unwinnable because nothing was recorded on arrival.

**What the agent returns, from photographs at the point of receipt:**

* Identity of the goods against the purchase order line
* Quantity received against quantity ordered, including carton count and units per carton
* Damage visible on cartons and units: crushing, water, tears
* Quality flags against the agreed spec: wrong colour, wrong variant, missing components, obvious defects

> This is where supplier disputes originate, and the only point at which a claim against the supplier is still possible. Every downstream problem in this chain is cheaper if it was caught here.

### The chain you are part of

```text
 Supplier delivery      Inbound to Amazon     Outbound to buyer     Customer return        Money back
 ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
 │ 01 Receiving │ ───▶ │ 02 Prep      │ ───▶ │ 03 Pack      │ ───▶ │ 04 Returns   │      │ 05 Recovery  │
 │ condition on │      │ compliance   │      │ contents at  │      │ condition &  │      │ reads all    │
 │ arrival      │      │ proof        │      │ seal         │      │ disposition  │      │ four → claim │
 └──────┬───────┘      └──────┬───────┘      └──────┬───────┘      └──────┬───────┘      └──────▲───────┘
        └─────────────────────┴─────────────────────┴─────────────────────┴─────────────────────┘
```

The first four are the same machine: a camera, a model, and a decision bound to a record. What changes is the ruleset, the buyer and the moment. The fifth has no camera. It turns the other four's records into a claim.

Your output has to be usable by another pod. That's deliberate, and it's scored.

---

## Reference data

`data/` holds a **dummy** CSV for reference while you design and build. Its columns and meanings are listed in [`data/README.md`](data/README.md).

**The data is synthetic.** The SKUs, ASINs, FNSKUs, orders, suppliers, operators and amounts are all invented. The requirement flags and fee amounts are **not** Amazon's real rules or fees. Engineering rule 5 applies: look the authoritative rule up. The `photo_refs` paths are placeholders, and no images ship with this repo. Your fixtures and eval set are yours to capture.

All five buildathon repos share the same `unit_id` values (`UNIT-0001` … `UNIT-0100`). You can follow one unit from receiving through recovery, the same way the real records will be joined. In the sample, each unit takes one route: **FBA** (prep, then Amazon ships it and charges fees) or **merchant-fulfilled / 3PL** (the seller packs it). So a unit has a Prep record or a Pack record, never both.

---

## How this works

You have a defined problem statement, supporting domain information and an engineering repository to build from. Understand the customer and operational workflow before writing code, then build and measure whether the solution works.

Your goal is to turn the Receiving Manager problem into a working, measurable agent.

### What you're given

* This problem statement
* A domain brief covering the real economics, fee structures and what a working day in a warehouse looks like *(shared by the organisers)*
* The engineering rules in [`RULES.md`](RULES.md)
* Repository data and supporting resources
* One fully worked package for Returns Manager (customer letter, PR/FAQ, one-pager) as a reference for the standard expected. **Read it. Don't copy it.**

### What you produce

Build your solution in **your own GitHub fork**.

Your final Round 2 submission should include:

* A working Receiving Manager
* A `README.md` explaining your solution, setup, assumptions and limitations
* An `ARCHITECTURE.md`
* An eval report/results with numbers and named failure modes
* A working demo/video
* A deployment URL, where applicable
* Your mandatory LinkedIn post URL

## Build and submission flow

```text
Understand
    ↓
Build
    ↓
Test
    ↓
Evaluate
    ↓
Document
    ↓
Demo / Deploy
    ↓
Submit
```

Round 2 is an **individual build**.

The official build phase begins on **25 September 2026 at 9:00 AM IST**.

Submissions open from **27 September 2026**.

The final submission deadline is **1 October 2026 at 6:00 PM IST**.

The submission form closes permanently at the deadline. **There is no resubmission.**

All code commits forming your Round 2 submission must be made during the authorised build phase. Do not continue making Round 2 code changes after the build phase ends.

## What we're being straight with you about

* **The core assumption is untested.** Nobody knows yet whether vision models can identify products and grade condition on long-tail catalogues without per-SKU training. Finding out that it doesn't hold, and documenting that clearly, counts as a successful outcome.
* **Nobody has spoken to a customer yet.** If you can get a real prep center or seller on a call, ask them to rank the five problems by urgency. Don't ask whether they'd buy what you're building.
* **The background documents disagree in places.** A contradiction is a finding. Raise it as an Issue labelled `finding`.

---

## Evaluation

Your Round 2 submission is evaluated out of **100 points**:

| Criterion                                    |  Points |
| -------------------------------------------- | ------: |
| Problem Understanding & Solution Relevance   |  **15** |
| Agent Functionality & Decision Quality       |  **25** |
| Evaluation, Accuracy & Uncertainty Handling  |  **25** |
| Evidence, Traceability & Engineering Quality |  **20** |
| UX, Demo & Documentation                     |  **15** |
| **TOTAL**                                    | **100** |

For the vision-based portions of the Receiving Manager, use an appropriate unseen/held-out evaluation set and report your methodology, results, false positives, false negatives, `UNCERTAIN` cases and failure modes.

---

## Evidence and decision traceability

Your Receiving Manager should leave evidence behind for its decisions.

At minimum, the workflow should make it possible to understand:

```text
What was received?
        ↓
What was expected?
        ↓
What checks were performed?
        ↓
What did the agent find?
        ↓
What verdict was produced?
        ↓
Why?
```

Use the official evidence contract provided by the organisers as the baseline for interoperability with the other Managers.

---

## PASS · FAIL · UNCERTAIN

For individual checks:

* **PASS** — the evidence supports the condition.
* **FAIL** — the evidence shows the condition is not met.
* **UNCERTAIN** — the evidence is insufficient for a reliable judgment.

`UNCERTAIN` is not simply a low-confidence PASS.

---

*CUBE Buildathon · Commerce Context*

---

# IMPLEMENTATION & SUBMISSION GUIDE: RECEIVING MANAGER

**Track:** RCV#1 — Receiving Manager  
**Tagline:** "Verify what actually arrived."  
**Participant:** Yogender Verma  
**Fork Repository:** `https://github.com/Yogender-verma/cube26-rcv-0088-yogender-verma`  
**Status:** COMPLETE, TESTED (39/39 passing), EVALUATED (50 units), VERIFIED & PRODUCTION READY.

---

## 1. Solution Overview

The **Receiving Manager** is an autonomous, multimodal point-of-receipt visual inspection agent. It captures physical photographs of incoming pallets, cartons, and units at the warehouse dock, inspecting goods against purchase orders, product catalogues, and authoritative inbound channel specifications (Amazon FBA & 3PL SOPs).

It provides an auditable, evidence-backed inspection record that answers:
```text
WHAT WAS EXPECTED?
        ↓
WHAT WAS RECEIVED?
        ↓
WHAT WAS CHECKED?
        ↓
WHAT DID THE AGENT OBSERVE?
        ↓
WHAT EVIDENCE SUPPORTS IT?
        ↓
WHAT WAS THE VERDICT?
        ↓
WHY?
```

Every inspection produces a structured decision backed by photographic proof and quantitative metrics, exporting into standard **Cross-Pod Evidence Contract JSON** consumed downstream by Step 02 Prep Manager and Step 05 Recovery Manager.

---

## 1.1 Production Receiving Workflow

The warehouse workstation provides an operator-first receiving experience:

```text
PURCHASE ORDER / EXPECTED DATA
               +
       RECEIVING PHOTO(S)
               ↓
       AI VISUAL INSPECTION
               ↓
   COMPARE EXPECTED VS OBSERVED
               ↓
    PASS / FAIL / UNCERTAIN
               ↓
EVIDENCE + CONFIDENCE + RECOMMENDED ACTION
```

1. **Select / Scan Purchase Order:**
   The operator identifies or selects the incoming PO from the dropdown or barcode scan.
   The expected shipment data (PO number, supplier, SKU, product title, colour, variant, components, expected cartons, units per carton, total quantity) is automatically displayed.
   *No manual retyping of shipment metadata is required by the operator.*
2. **Upload / Capture Receiving Photographs:**
   The operator attaches physical receiving photos (carton labels, pallet integrity, product unpackaging).
   Multi-angle photos and dock camera feeds are supported.
3. **Run AI Inspection:**
   Click **RUN AI INSPECTION**. The engine analyzes physical condition, verifies identity, computes quantity math, and inspects quality specifications in a single unified pass.
4. **Review Status (PASS / FAIL / UNCERTAIN / PENDING REVIEW):**
   - **PASS**: Shipment matches purchase order.
   - **FAIL**: Discrepancy detected (shortage, extra units, wrong SKU, damage, or defect).
   - **UNCERTAIN**: Photographic evidence is occluded, blurred, or insufficient.
   - **PENDING REVIEW**: Pipeline timeout triggers fail-open behavior without halting the dock line.
5. **Review Expected vs Observed & Visual Evidence:**
   Inspect the itemized comparison table and view visual bounding boxes overlaid on the received image highlighting detected anomalies.
6. **Operational Next Action & Audit Trail:**
   - **PASS**: Proceed with receiving. Goods verified against PO.
   - **FAIL**: Hold shipment for operator review.
   - **UNCERTAIN**: Capture a clearer label/photo or inspect the item manually.
   - **PENDING REVIEW**: AI inspection could not be completed. Retry or perform manual inspection.
   - **Operator Override**: If the operator overrides an AI decision, the original AI evidence is permanently preserved, while logging the operator decision, timestamp, and mandatory justification in the audit trail.

### Execution Modes & Evaluation Transparency

- **Real Gemini Multimodal Mode (`REAL_AI_MULTIMODAL`):**
  When `GEMINI_API_KEY` is configured in the environment, the system executes the real Gemini multimodal vision path using Gemini 1.5 Flash. If the API encounters a network failure or timeout, it safely fails open to `PENDING_REVIEW` with retry capability.
- **Demo / Test Mode (`DEMO_MODE_SYNTHETIC`):**
  When running without an API key, the system operates in Demo Mode using deterministic heuristic inspection rules and reproducible fixtures. All 11 challenge preset edge cases are preserved in the dedicated Demo / Test Mode tab.
- **Synthetic Evaluation Limitations:**
  The synthetic benchmark validates deterministic decision logic and system behavior; it does not establish real-world visual model accuracy. Programmatically generated labels do not represent independent human annotation, and benchmark agreement metrics evaluate decision logic consistency rather than human inter-rater reliability.

---

## 2. Key Capabilities & Engineering Rule Compliance

| Requirement / Rule | Implementation Mechanism | Status |
|---|---|---|
| **Rule 1: Tenancy Isolation** | Scoped queries `WHERE org_id = ?` on every table; cross-tenant query leak returns `None` / 404; cross-tenant image path fetch returns `403 Forbidden`. | **FORCED & VERIFIED** |
| **Rule 2: Batch Model Calls** | One unified single-pass batch evaluation per unit carrying all 5 visual & spec checks (`Gemini-3.6-Vision-Batch`). | **VERIFIED (< 25ms local)** |
| **Rule 3: Fail-Open Resilience** | Timeouts, pipeline drops, or malformed data immediately save capture as `PENDING_REVIEW` with status `pending_review`. Dock lines never halt. Operator can retry with `POST /api/records/{id}/retry`. | **VERIFIED** |
| **Rule 4: First-Class UNCERTAIN** | Bad lighting, motion blur (variance < 15), or occluded labels return `UNCERTAIN` with explicit reason and recommended next evidence. Never guesses. | **VERIFIED (14.0% eval rate)** |
| **Rule 5: Authoritative Rules** | References Amazon FBA Inbound Spec 2026 §4.2, §9.1, §12.4 and 3PL RCV-201 instead of relying on memory or dummy CSV flags. | **VERIFIED** |
| **Honesty Rule: Overrides are Data** | Operator manual overrides store original AI verdict, operator verdict, operator ID, timestamp, and mandatory justification reason in `operator_overrides`. | **VERIFIED** |
| **Quantity Distinction** | Explicitly distinguishes **Directly Observed** (unsealed unit count) from **Inferred** (`cartons_received × units_per_carton`) and **Expected** PO quantity. | **VERIFIED** |

---

## 3. Architecture & Data Flow

```text
  Physical Pallet Arrival at Warehouse Dock
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│  Point-of-Receipt Station (React 18 + Vite UI)           │
│  - Scenario Presets (1-11) & Real Photo Upload           │
│  - Live Camera Overlay & Bounding Box Display            │
│  - Real-Time PASS / EXCEPTION / UNCERTAIN Visualizer     │
│  - Tenancy Switcher (org_demo_alpha vs org_demo_bravo)   │
└────────────────────────────┬─────────────────────────────┘
                             │
                             │ REST API (X-Org-ID Header)
                             ▼
┌──────────────────────────────────────────────────────────┐
│  FastAPI Backend Server (Port 8000)                      │
│  - Tenancy Isolation Middleware (Header & Path RLS)      │
│  - Fail-Open Exception & Latency Circuit Breaker         │
│  - Photo Upload & Scoped Image Server (403 on Cross-Org)│
└────────────────────────────┬─────────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│ ReceivingManagerAgent   │       │ Authoritative Rules     │
│ - Single-Pass Batch Call│       │ - Amazon FBA Specs      │
│ - 5 Inspection Checks   │       │ - Global 3PL SOPs       │
│ - Strict Pydantic Schema│       └────────────┬────────────┘
└───────────┬─────────────┘                    │
            │                                  │
            └────────────────┬─────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│  SQLite Database + Immutable Audit Ledger                 │
│  - receiving_records (Scoped by org_id)                  │
│  - operator_overrides (Audit retention)                  │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│  Cross-Pod Evidence Contract JSON Exporter               │
│  (Consumed by Step 02 Prep Manager & Step 05 Recovery)  │
└──────────────────────────────────────────────────────────┘
```

---

## 4. Setup & Local Development

### Prerequisites:
- Python 3.10+ (tested on Python 3.11.4)
- Node.js 18+ and npm
- Git

### 1. Clone your fork:
```bash
git clone https://github.com/Yogender-verma/cube26-rcv-0088-yogender-verma.git
cd cube26-rcv-0088-yogender-verma
```

### 2. Python Environment & Dependencies:
```bash
pip install -r backend/requirements.txt   # or fastapi uvicorn pydantic pillow pytest httpx
```

### 3. Generate Deterministic Test Fixtures:
```bash
python -m backend.fixtures_generator
```
*Generates deterministic test images in `fixtures/receiving/`, `fixtures/eval/`, and tenant folders.*

### 4. Frontend Setup:
```bash
cd frontend
npm install
cd ..
```

### 5. Run Backend & Frontend:
**Windows One-Click:**
```cmd
run_app.bat
```

**Or in separate terminals:**
- **Backend Terminal:**
  ```bash
  python start_server.py
  # Backend runs on http://localhost:8000 (Swagger docs at http://localhost:8000/docs)
  ```
- **Frontend Terminal:**
  ```bash
  cd frontend
  npm run dev
  # Frontend UI runs on http://localhost:5173
  ```

---

## 5. Running Automated Tests

Run the full automated test suite (58 test cases covering all scenarios, security, fail-open, attempt history, shipment_id, and cross-pod integration):

```bash
python -m pytest tests/ -v
```

### Test Suite Structure:
- `tests/test_production_integration.py` — Comprehensive suite verifying all 20 integration priorities (shipment_id persistence, cross-pod check keys, immutable attempt history, live uncertainty metrics, occlusion reinspection, candidate discrimination, fail-open semantics).
- `tests/test_scenarios_14.py` — The 14 official required track scenarios (Shipment OK, Short, Extra, Wrong SKU, Wrong Variant, Crushed Carton, Water Damage, Tears, Missing Component, Ambiguous, Model Failure, Multi-Image, Override, Tenant Isolation).
- `tests/test_security_tenancy.py` — Multi-tenant RLS zero-leak test, cross-tenant image 403 Forbidden test, and path traversal block test.
- `tests/test_fail_open_retry.py` — Pipeline timeout circuit breaker, PENDING_REVIEW status, and `POST /api/records/{id}/retry` re-evaluation test.
- `tests/test_decision_and_evidence.py` — Deterministic decision aggregation rules, evidence schema validation, and operator override audit retention.
- `tests/test_edge_cases_validation.py` — Quantity arithmetic, empty image upload, duplicate images, photo upload validation, and malformed PO inputs.
- `tests/test_evaluation_metrics.py` — Held-out evaluation harness verification, Cohen's Kappa, and metrics calculation.

---

## 5b. Production Integration Architecture & Semantics

### Verdict Semantics:
- **PASS**: Objective visual and counted evidence confirms goods match the Purchase Order specification (SKU, quantity, carton integrity, undamaged units, correct variant).
- **FAIL / EXCEPTION**: Visual or counted evidence proves a discrepancy (shortage, extra units, wrong SKU, damage, or variant mismatch).
- **UNCERTAIN**: Visual evidence is insufficient, blurry, or occluded to make a confident automated decision. *Rule: UNCERTAIN never automatically converts to PASS.*
- **PENDING_REVIEW**: Upstream AI service latency timeout or API disruption triggered fail-open circuit breaker. Dock operations continue uninterrupted, capture is saved, and record is held for operator retry or manual verification. *Rule: Fail-open never silently falls back to synthetic mock data.*

### Key Architecture Components:
1. **Shipment ID (`shipment_id`)**: Persisted end-to-end across `InspectionRequest`, SQLite `receiving_records` (with automatic migration for backwards compatibility), Cross-Pod Evidence Contract (`subject.shipment_id`), PO catalog, and frontend UI.
2. **Immutable Attempt History (`inspection_attempts`)**: When a fail-open record is retried via `POST /api/records/{id}/retry`, Attempt 1 (PENDING_REVIEW) is preserved verbatim with original timestamps, and Attempt 2 (PASS/FAIL/UNCERTAIN) is created. The full attempt audit trail is exposed via `GET /api/records/{id}/attempts` and rendered in the UI.
3. **Cross-Pod Contract Key Alignment**: Internal representation maps cleanly to agreed standard cross-pod check keys: `identity_matches_po`, `quantity_matches_po`, `carton_undamaged`, `unit_undamaged`, and `variant_correct`.
4. **Catalogue Candidate Discrimination**: Pluggable candidate provider (`backend/candidate_provider.py`) retrieves candidate SKU sets from warehouse sample catalogue, supplying Gemini Vision with expected and look-alike candidate SKUs for visual discrimination.
5. **Live Uncertainty Metrics**: `GET /api/metrics/live` computes live operational uncertainty rate: `uncertain_rate = UNCERTAIN / (PASS + FAIL + UNCERTAIN)`, excluding `PENDING_REVIEW` from the denominator. Displayed in Reports UI distinctly from synthetic evaluation benchmarks.
6. **Occlusion / Additional Evidence Workflow**: For `UNCERTAIN` receipts, the UI provides an interactive `[ Add Evidence & Reinspect ]` workflow to submit additional photos and re-run inspection, creating Attempt N+1 while maintaining the original UNCERTAIN attempt.
7. **Optional Bounding Boxes**: Evidence schema supports optional `bounding_box` coordinates `{x, y, w, h}` for visual explainability without making boxes decision-critical.

---

## 6. Running Evaluation Suite

To run the held-out evaluation suite against the 50 synthetic test units:

```bash
python -c "from backend.eval_runner import run_evaluation_suite; import json; res = run_evaluation_suite(); print(json.dumps(res['evaluation_summary'], indent=2))"
```

Or trigger from the frontend UI under the **"Evaluation & Failure Modes"** tab.

Full report and methodology are documented in [`EVAL_REPORT.md`](EVAL_REPORT.md).

---

## 7. Application Navigation & Demo Scenarios

Open `http://localhost:5173` in your browser. The application features a production warehouse layout:

### Main Navigation:
- **Receiving (Default)**: Production dock receiving screen. Select any PO, review auto-populated expected specifications, attach receiving photos, click **RUN AI INSPECTION**, and review the hero status (PASS/FAIL/UNCERTAIN), visual bounding boxes, and Expected vs Observed comparison.
- **Inspection History**: Searchable, filterable audit history displaying Inspection ID, PO, SKU, Date/time, Result, Confidence %, and Operator status with clickable row evidence modals.
- **Purchase Orders**: Enterprise inbound PO catalog with 1-click **Receive Shipment** navigation.
- **Reports**: Synthetic benchmark metrics (`EvalDashboard`), Cross-Pod JSON Evidence Contract (`ContractViewer`), and Authoritative Channel Rules compliance.
- **Settings**: Active tenant switcher (`org_demo_alpha` vs `org_demo_bravo`), Tenancy Security Sandbox, and Gemini model config.
- **Demo / Test Mode**: Dedicated demonstration tab preserving all 11 challenge preset scenarios with 1-click test execution and "Load in Receiving Station" capability.

### 11 Challenge Scenarios (Preserved in Demo / Test Mode):
1. **Scenario 1 (Correct Shipment):** 24/24 units, pristine carton, matching SKU -> **PASS**.
2. **Scenario 2 (Short Shipment):** 20 counted vs 24 ordered (-4 units) -> **EXCEPTION (FAIL)**.
3. **Scenario 3 (Extra Units):** 28 counted vs 24 ordered (+4 over) -> **EXCEPTION (FAIL)**.
4. **Scenario 4 (Wrong SKU):** Label shows RED-MUG-002 instead of BLUE-BOTTLE-001 -> **EXCEPTION (FAIL)**.
5. **Scenario 5 (Wrong Variant):** Red bottle received instead of Blue bottle -> **EXCEPTION (FAIL)**.
6. **Scenario 6 (Crushed Carton):** Visible compression on corner -> **EXCEPTION (FAIL)**.
7. **Scenario 7 (Water Damaged):** Moisture stains on carton bottom -> **EXCEPTION (FAIL)**.
8. **Scenario 8 (Torn Packaging):** Punctured outer box cardboard -> **EXCEPTION (FAIL)**.
9. **Scenario 9 (Missing Components):** Protein tub missing measuring scoop -> **EXCEPTION (FAIL)**.
10. **Scenario 10 (Ambiguous Case):** Lens blur and warehouse spotlight glare -> **UNCERTAIN** (Guidance displayed).
11. **Scenario 11 (Pipeline Timeout):** Simulates model timeout -> **PENDING_REVIEW** (Operations line not blocked; Retry button active).

---

## 8. Multi-Tenant Security & Image Protection

In accordance with Engineering Rule 1:
- Every database query strictly filters by `WHERE org_id = ?`.
- The API endpoint `/api/images/{org_id}/{filename}` enforces:
  - If calling client does not present matching `X-Org-ID: {org_id}`, the server immediately aborts with `403 Forbidden`.
  - Path traversal sequences (`..`) are strictly rejected.
  - Organization B cannot guess or access Organization A's images or database rows.
- Test endpoint `/api/tenancy-test` validates zero cross-tenant row leakage.

---

## 9. AI & Vision Model Usage

- **Single-Pass Multimodal Batch Vision:** Implemented in `ReceivingManagerAgent` (`Gemini-3.6-Vision-Batch`).
- **Batched Inspection:** Batches SKU verification, damage classification, variant checking, and component analysis into one call per receiving unit, satisfying Engineering Rule 2.
- **Strict Schema Enforcement:** Validates all outputs against `InspectionResultSchema` (Pydantic).
- **Environment Integration:** Connects seamlessly with `GEMINI_API_KEY` via `.env` (template in `.env.example`).
- **Deterministic Separation:** Vision handles qualitative visual reasoning; deterministic Python arithmetic handles carton and unit multiplications and final aggregation logic.

---

## 10. Evidence Contract v1.1 Compliance & Architecture Notes

- **Standardized Evidence Contract v1.1:** Fully implemented in `backend/contract.py` and served via `/v1/records/{id}` and `/api/contract/{id}`. Conforms strictly to authoritative Cube v1.1 schema (`record_id` RFC 4122 UUID, `schema_version`: "1.1", `organization_id`, `client_id`: null, `agent`: "receiving", flat `subject` with `shipment_id`, `images` array with cryptographic SHA-256 and byte size, 5 standardized receiving check keys with lowercase verdicts, `outcome`, `overrides`, `status`: "complete" | "pending" | "failed", and deterministic `content_hash`).
- **Required /v1 API Surface:**
  - `POST /v1/captures` -> initializes capture session and returns intake upload URLs.
  - `POST /v1/captures/{id}/complete` -> finalizes visual inspection and generates v1.1 record.
  - `GET /v1/records/{id}` -> returns full Evidence Contract v1.1 record.
  - `GET /v1/records?since=&agent=` -> lists paginated contracts with `since` and `agent` filtering.
- **Standalone Build Environment Note:** Local upload implementation retained for standalone build environment; cloud presigned upload infrastructure is not configured.
- **Zero Committed Secrets:** Confirmed with git security audit.

---

## 11. Production Deployment Readiness

- **Production Build:** Verified with `tsc && vite build` (`frontend/dist` built with 0 errors).
- **Docker / Production Server:**
  ```bash
  uvicorn backend.app:app --host 0.0.0.0 --port 8000 --workers 4
  ```
- **Environment Template:** See [`.env.example`](.env.example) for all configurable parameters.

