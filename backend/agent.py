"""
Receiving Manager Agent Engine (Step 01 of 5 in Commerce Stream)
Implements unified single-pass batch vision analysis, fail-open execution,
uncertainty scoring, authoritative rule checking, and evidence generation.
"""

import time
import json
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.rules_engine import evaluate_authoritative_compliance

class ReceivingManagerAgent:
    def __init__(self, model_name: str = "Gemini-3.6-Vision-Batch"):
        self.model_name = model_name

    def run_batch_receiving_inspection(
        self,
        org_id: str,
        unit_id: str,
        po_line_spec: Dict[str, Any],
        captured_images: List[str],
        simling_failure: bool = False
    ) -> Dict[str, Any]:
        """
        Engineering Rule 2: Makes ONE single batch call per unit carrying ALL checks:
        1. Identity match against PO line
        2. Quantity count (cartons & units per carton)
        3. Carton damage (crushing, water, tears, none)
        4. Unit damage (crushing, water, tears, none)
        5. Quality flags (wrong_colour, wrong_variant, missing_components, obvious_defect)

        Engineering Rule 3 (Fail Open):
        If an exception or timeout occurs, capture is preserved and output is marked 'pending_review'.
        Warehouse operators are never blocked.
        """
        captured_at = datetime.utcnow().isoformat()
        
        # Engineering Rule 3: Fail-Open Simulation / Error Handling
        if simling_failure:
            return self._build_fail_open_response(
                org_id, unit_id, po_line_spec, captured_images, captured_at,
                reason="Model service timeout / vision pipeline latency spike (Saved as Pending Review)"
            )

        try:
            # Execute Single-Pass Unified Vision & Logic Batch Evaluation
            start_time = time.time()
            
            # Analyze photo quality / visual clarity
            image_clarity_score = self._assess_image_clarity(captured_images)
            
            # 1. Identity Match Check
            id_match, id_conf, id_reason = self._check_identity(po_line_spec, image_clarity_score)
            
            # 2. Quantity Count Verification
            qty_ordered = po_line_spec.get("qty_ordered", 12)
            cartons_ordered = po_line_spec.get("cartons_ordered", 1)
            units_per_carton = po_line_spec.get("units_per_carton_ordered", 12)
            
            # Simulate counted values from image fixtures / spec
            cartons_rec = po_line_spec.get("cartons_received", cartons_ordered)
            units_rec_per_carton = po_line_spec.get("units_per_carton_counted", units_per_carton)
            total_qty_rec = cartons_rec * units_rec_per_carton
            
            qty_verdict = "PASS" if total_qty_rec == qty_ordered else "FAIL"
            qty_conf = 0.98 if image_clarity_score > 0.6 else 0.50
            
            # 3 & 4. Carton & Unit Damage Inspection
            carton_dmg, unit_dmg, dmg_conf = self._check_damage(captured_images, image_clarity_score)
            
            # 5. Quality Flags against agreed Spec
            q_flags, q_conf = self._check_quality_flags(po_line_spec, image_clarity_score)
            
            # Determine Overall Verdict (PASS, FAIL, UNCERTAIN)
            # Engineering Rule 4: UNCERTAIN is a valid first-class verdict
            if image_clarity_score < 0.4 or id_match == "uncertain" or carton_dmg == "uncertain" or unit_dmg == "uncertain":
                overall_verdict = "UNCERTAIN"
                overall_conf = min(id_conf, dmg_conf, q_conf, 0.49)
            elif id_match == "no" or qty_verdict == "FAIL" or carton_dmg in ["crushing", "water", "tears"] or unit_dmg in ["crushing", "water", "tears"] or bool(q_flags):
                overall_verdict = "FAIL"
                overall_conf = max(id_conf, dmg_conf, q_conf)
            else:
                overall_verdict = "PASS"
                overall_conf = (id_conf + qty_conf + dmg_conf + q_conf) / 4.0

            # Rule 5: Evaluate Authoritative Channel Compliance
            receiving_data_for_rules = {
                "carton_damage": carton_dmg,
                "unit_damage": unit_dmg,
                "quality_flags": ";".join(q_flags) if isinstance(q_flags, list) else q_flags,
                "qty_ordered": qty_ordered,
                "qty_received": total_qty_rec
            }
            authoritative_compliance = evaluate_authoritative_compliance(receiving_data_for_rules)
            
            elapsed_ms = round((time.time() - start_time) * 1000, 2)

            # Build Evidence Pipeline Structure
            evidence_trail = {
                "what_received": {
                    "cartons_received": cartons_rec,
                    "units_per_carton": units_rec_per_carton,
                    "total_qty_received": total_qty_rec,
                    "photo_refs": captured_images
                },
                "what_expected": {
                    "po_number": po_line_spec.get("po_number", "PO-7000"),
                    "po_line": po_line_spec.get("po_line", 1),
                    "supplier": po_line_spec.get("supplier", "Supplier East"),
                    "sku": po_line_spec.get("sku", "SKU-SAMPLE"),
                    "asin": po_line_spec.get("asin", "B0DUMMY000"),
                    "product_title": po_line_spec.get("product_title", "Sample Product"),
                    "spec": {
                        "colour": po_line_spec.get("spec_colour", "n/a"),
                        "variant": po_line_spec.get("spec_variant", "n/a"),
                        "components": po_line_spec.get("spec_components", "n/a")
                    },
                    "cartons_ordered": cartons_ordered,
                    "qty_ordered": qty_ordered
                },
                "checks": [
                    {
                        "check_name": "Identity Match",
                        "verdict": "PASS" if id_match == "yes" else ("FAIL" if id_match == "no" else "UNCERTAIN"),
                        "confidence": id_conf,
                        "details": f"Visual identity check: {id_reason}"
                    },
                    {
                        "check_name": "Quantity Verification",
                        "verdict": qty_verdict,
                        "confidence": qty_conf,
                        "details": f"Counted {total_qty_rec} units ({cartons_rec} cartons x {units_rec_per_carton} units) vs {qty_ordered} ordered."
                    },
                    {
                        "check_name": "Carton Damage",
                        "verdict": "PASS" if carton_dmg == "none" else ("UNCERTAIN" if carton_dmg == "uncertain" else "FAIL"),
                        "confidence": dmg_conf,
                        "details": f"Carton state evaluated as '{carton_dmg}'"
                    },
                    {
                        "check_name": "Unit Damage",
                        "verdict": "PASS" if unit_dmg == "none" else ("UNCERTAIN" if unit_dmg == "uncertain" else "FAIL"),
                        "confidence": dmg_conf,
                        "details": f"Unit state evaluated as '{unit_dmg}'"
                    },
                    {
                        "check_name": "Spec Quality",
                        "verdict": "PASS" if not q_flags else "FAIL",
                        "confidence": q_conf,
                        "details": f"Quality flags detected: {', '.join(q_flags)}" if q_flags else "Agreed spec confirmed."
                    }
                ],
                "authoritative_channel_checks": authoritative_compliance,
                "verdict": overall_verdict,
                "rationale": f"Batch decision produced in {elapsed_ms}ms with {round(overall_conf*100, 1)}% confidence."
            }

            return {
                "unit_id": unit_id,
                "org_id": org_id,
                "captured_at": captured_at,
                "batch_execution_time_ms": elapsed_ms,
                "batch_single_pass": True,
                "identity_match": id_match,
                "cartons_ordered": cartons_ordered,
                "cartons_received": cartons_rec,
                "units_per_carton_ordered": units_per_carton,
                "units_per_carton_counted": units_rec_per_carton,
                "qty_ordered": qty_ordered,
                "qty_received": total_qty_rec,
                "carton_damage": carton_dmg,
                "unit_damage": unit_dmg,
                "quality_flags": ";".join(q_flags) if isinstance(q_flags, list) else q_flags,
                "overall_verdict": overall_verdict,
                "agent_confidence": round(overall_conf, 2),
                "status": "processed",
                "evidence_data": json.dumps(evidence_trail)
            }

        except Exception as err:
            return self._build_fail_open_response(
                org_id, unit_id, po_line_spec, captured_images, captured_at,
                reason=f"Pipeline exception: {str(err)} (Saved as Pending Review)"
            )

    def _assess_image_clarity(self, images: List[str]) -> float:
        """Evaluates image resolution, lighting, and occlusion."""
        if not images:
            return 0.2
        # Check image path keywords for mock blurred/glare conditions
        for img in images:
            if "blur" in img.lower() or "dark" in img.lower() or "occluded" in img.lower():
                return 0.35
        return 0.92

    def _check_identity(self, spec: Dict[str, Any], clarity: float) -> tuple:
        if clarity < 0.4:
            return "uncertain", 0.40, "Image resolution insufficient to resolve product text / barcode."
        override_match = spec.get("override_identity_match")
        if override_match:
            return override_match, 0.95, f"Verified against PO line SKU {spec.get('sku')}."
        # Default match logic
        return "yes", 0.94, f"Visual features match PO line product '{spec.get('product_title')}'."

    def _check_damage(self, images: List[str], clarity: float) -> tuple:
        if clarity < 0.4:
            return "uncertain", "uncertain", 0.35
        # Check if photos indicate specific simulated damage
        for img in images:
            img_l = img.lower()
            if "crushing" in img_l:
                return "crushing", "none", 0.91
            if "water" in img_l:
                return "water", "water", 0.89
            if "tears" in img_l:
                return "tears", "tears", 0.92
        return "none", "none", 0.95

    def _check_quality_flags(self, spec: Dict[str, Any], clarity: float) -> tuple:
        if clarity < 0.4:
            return [], 0.40
        flags = spec.get("override_quality_flags", [])
        if isinstance(flags, str):
            flags = [f.strip() for f in flags.split(";") if f.strip()]
        return flags, 0.93

    def _build_fail_open_response(
        self, org_id: str, unit_id: str, spec: Dict[str, Any],
        images: List[str], captured_at: str, reason: str
    ) -> Dict[str, Any]:
        """Constructs a safe fail-open capture record that never blocks warehouse operations."""
        evidence = {
            "what_received": {"photo_refs": images},
            "what_expected": spec,
            "checks": [
                {"check_name": "Batch Inspection", "verdict": "UNCERTAIN", "confidence": 0.0, "details": reason}
            ],
            "verdict": "PENDING_REVIEW",
            "rationale": f"FAIL-OPEN EXECUTION: {reason}"
        }
        return {
            "unit_id": unit_id,
            "org_id": org_id,
            "captured_at": captured_at,
            "batch_execution_time_ms": 0.0,
            "batch_single_pass": True,
            "identity_match": "uncertain",
            "cartons_ordered": spec.get("cartons_ordered", 1),
            "cartons_received": spec.get("cartons_received", 1),
            "units_per_carton_ordered": spec.get("units_per_carton_ordered", 12),
            "units_per_carton_counted": spec.get("units_per_carton_counted", 12),
            "qty_ordered": spec.get("qty_ordered", 12),
            "qty_received": spec.get("qty_received", 12),
            "carton_damage": "uncertain",
            "unit_damage": "uncertain",
            "quality_flags": "",
            "overall_verdict": "PENDING_REVIEW",
            "agent_confidence": 0.0,
            "status": "pending_review",
            "evidence_data": json.dumps(evidence)
        }
