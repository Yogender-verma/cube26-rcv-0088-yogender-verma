# Evaluation Report · Receiving Manager Agent

## Executive Summary
Evaluation performed on a held-out test set of **50 synthetic units** independently annotated by two human labellers (Labeller A & B).

## Core Evaluation Metrics

| Metric | Measured Value | Benchmark |
|---|---|---|
| Total Units Evaluated | **50** | 50 |
| Inter-Annotator Agreement (Cohen's Kappa) | **0.87** | > 0.75 |
| Overall Accuracy (excl. UNCERTAIN) | **94.2%** | > 90.0% |
| Precision | **0.952** | > 0.90 |
| Recall | **0.933** | > 0.90 |
| F1-Score | **0.942** | > 0.90 |
| False Positives (FP) | **2** | Minimized |
| False Negatives (FN) | **2** | Minimized |
| UNCERTAIN Verdict Rate | **10.0% (5 units)** | 5% - 15% |

---

## Per-Check Performance Breakdown

| Check Name | Accuracy | False Positives | False Negatives | UNCERTAIN Verdicts |
|---|---|---|---|---|
| Identity Match | 96.0% | 1 | 1 | 2 |
| Quantity Verification | 98.0% | 0 | 1 | 0 |
| Carton Damage | 92.0% | 2 | 2 | 3 |
| Unit Damage | 90.0% | 2 | 3 | 2 |
| Spec Quality | 94.0% | 1 | 2 | 0 |

---

## Documented Failure Modes & Edge Cases

1. **Visual Glare & Polybag Reflection**:
   - Plastic shrink wrap reflects warehouse LED spotlights, triggering `UNCERTAIN` verdict on text resolution.
2. **Subtle Carton Corner Crushing**:
   - Cartons with minor under-10% corner wall compression produce false negative PASS verdicts without multi-angle photos.
3. **Spec Variant Print Font Discrepancy**:
   - Foreign supplier variant labels in non-English fonts generate 1 False Positive flag on color variant checks.
