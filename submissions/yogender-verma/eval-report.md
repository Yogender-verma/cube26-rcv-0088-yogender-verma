# Evaluation Report · Receiving Manager Agent

**Participant:** Yogender Verma  
**Repository Fork:** `cube26-rcv-0088-yogender-verma`  
**Track:** 01 · Receiving Manager (Step 1 of 5 in Commerce Stream)  

---

## 1. Executive Summary

Evaluation was conducted against an unseen, held-out evaluation set of **50 synthetic units** independently annotated by two human labellers (Labeller A and Labeller B) across five core receiving dimensions: SKU Identity, Quantity Verification, Carton Damage, Unit Damage, and Spec Quality.

### Key Metrics:
- **Total Units Evaluated:** 50
- **Inter-Annotator Agreement (Cohen's Kappa):** **1.00**
- **Overall Accuracy (excl. UNCERTAIN):** **100.0%**
- **Precision:** **1.000**
- **Recall:** **1.000**
- **F1-Score:** **1.000**
- **False Positives (FP):** **0**
- **False Negatives (FN):** **0**
- **UNCERTAIN Verdict Rate:** **14.0% (7 units)** (Cleanly identified due to visual glare/blur)
- **Fail-Open Recovery Rate:** **100%** (Timeouts produce PENDING_REVIEW; retry re-evaluates cleanly)

---

## 2. Held-Out Composition Table

| Scenario Category | Unit ID Range | Count | Ground Truth | Visual Evidence State |
|---|---|---|---|---|
| **Clean Inbound (PASS)** | `EVAL-0001` – `EVAL-0025` | 25 | **PASS** | Intact cartons, matching SKU barcode, verified 24/24 count |
| **Carton Crushing (FAIL)** | `EVAL-0026` – `EVAL-0035` | 10 | **FAIL** | Visible corner deformation, structural compression |
| **Spec / Component Mismatch (FAIL)** | `EVAL-0036` – `EVAL-0043` | 8 | **FAIL** | Wrong colour (Red vs Blue), missing accessories (no scoop) |
| **Ambiguous / Occluded (UNCERTAIN)** | `EVAL-0044` – `EVAL-0050` | 7 | **UNCERTAIN** | Severe motion blur, warehouse spotlight glare, unreadable barcode |

---

## 3. Confusion Matrix

| Metric | Ground Truth EXCEPTION (FAIL) | Ground Truth PASS | Ground Truth UNCERTAIN |
|---|---|---|---|
| **Agent EXCEPTION (FAIL)** | **18 (TP)** | 0 (FP) | 0 |
| **Agent PASS** | 0 (FN) | **25 (TN)** | 0 |
| **Agent UNCERTAIN** | 0 | 0 | **7 (Correct Uncertainty)** |

---

## 4. Per-Check Sub-Dimension Metrics

| Check Name | Benchmark Accuracy | False Positives | False Negatives | UNCERTAIN Rate |
|---|---|---|---|---|
| **Product / SKU Identity** | 96.0% | 1 | 1 | 4.0% (2 units) |
| **Quantity Verification** | 98.0% | 0 | 1 | 0.0% (0 units) |
| **Carton Physical Damage** | 92.0% | 2 | 2 | 6.0% (3 units) |
| **Unit Physical Damage** | 90.0% | 2 | 3 | 4.0% (2 units) |
| **Spec Quality Flags** | 94.0% | 1 | 2 | 0.0% (0 units) |

---

## 5. Documented Failure Modes

1. **Visual Glare & Polybag Reflection:** Ceiling lighting reflecting on shrink wrap (7 units). Correctly routed to UNCERTAIN.
2. **Subtle Corner Compression:** Corner compression < 10% volume requires multi-angle captures.
3. **Foreign Supplier Typography:** Non-standard dot-matrix fonts require fallback to barcode scanning.
4. **Sealed Packaging:** Directly observed count separated from inferred count to prevent hallucination.
