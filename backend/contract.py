"""
Cross-Pod Evidence Contract Generator (Receiving Manager -> Prep & Recovery Managers)
Standardized schema specification and serializer for Step 01 Receiving output.
Implements:
- Priority 1: shipment_id end-to-end (subject.shipment_id)
- Priority 3: Cross-pod check key alignment (identity_matches_po, quantity_matches_po, carton_undamaged, unit_undamaged, variant_correct)
- Priority 8: Optional bounding_box in evidence check items
- Priority 9: Standardized Evidence Contract Schema V1
"""

from typing import Dict, Any, Optional
import json
from datetime import datetime

RECEIVING_EVIDENCE_SCHEMA_V1 = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "ReceivingManagerEvidenceRecord",
    "type": "object",
    "required": [
        "schema_version",
        "record_id",
        "unit_id",
        "org_id",
        "captured_at",
        "stage",
        "subject",
        "po_line_reference",
        "checks",
        "inspection_findings",
        "verdict",
        "proof_of_receipt"
    ],
    "properties": {
        "schema_version": {"type": "string", "enum": ["1.0.0"]},
        "record_id": {"type": "string"},
        "unit_id": {"type": "string"},
        "shipment_id": {"type": ["string", "null"]},
        "org_id": {"type": "string"},
        "stage": {"type": "string", "enum": ["01_RECEIVING"]},
        "captured_at": {"type": "string"},
        "operator_id": {"type": "string"},
        "subject": {
            "type": "object",
            "required": ["unit_id", "shipment_id", "po_line_reference"],
            "properties": {
                "unit_id": {"type": "string"},
                "shipment_id": {"type": ["string", "null"]},
                "po_line_reference": {"type": "object"}
            }
        },
        "po_line_reference": {
            "type": "object",
            "required": ["po_number", "po_line", "sku", "asin", "qty_ordered"],
            "properties": {
                "po_number": {"type": "string"},
                "po_line": {"type": "integer"},
                "supplier": {"type": "string"},
                "sku": {"type": "string"},
                "asin": {"type": "string"},
                "product_title": {"type": "string"},
                "spec": {
                    "type": "object",
                    "properties": {
                        "colour": {"type": "string"},
                        "variant": {"type": "string"},
                        "components": {"type": "string"}
                    }
                },
                "qty_ordered": {"type": "integer"}
            }
        },
        "checks": {
            "type": "object",
            "required": [
                "identity_matches_po",
                "quantity_matches_po",
                "carton_undamaged",
                "unit_undamaged",
                "variant_correct"
            ],
            "properties": {
                "identity_matches_po": {
                    "type": "object",
                    "required": ["check_key", "verdict", "confidence"],
                    "properties": {
                        "check_key": {"type": "string", "enum": ["identity_matches_po"]},
                        "verdict": {"type": "string", "enum": ["PASS", "FAIL", "UNCERTAIN"]},
                        "expected_value": {"type": "string"},
                        "observed_value": {"type": "string"},
                        "confidence": {"type": "number"},
                        "details": {"type": "string"},
                        "timestamp": {"type": "string"},
                        "image_identifier": {"type": ["string", "null"]},
                        "bounding_box": {
                            "type": ["object", "null"],
                            "properties": {
                                "x": {"type": "number"},
                                "y": {"type": "number"},
                                "width": {"type": "number"},
                                "height": {"type": "number"}
                            }
                        }
                    }
                },
                "quantity_matches_po": {
                    "type": "object",
                    "required": ["check_key", "verdict", "confidence"],
                    "properties": {
                        "check_key": {"type": "string", "enum": ["quantity_matches_po"]},
                        "verdict": {"type": "string", "enum": ["PASS", "FAIL", "UNCERTAIN"]},
                        "expected_value": {"type": "string"},
                        "observed_value": {"type": "string"},
                        "confidence": {"type": "number"},
                        "details": {"type": "string"},
                        "timestamp": {"type": "string"},
                        "image_identifier": {"type": ["string", "null"]},
                        "bounding_box": {"type": ["object", "null"]}
                    }
                },
                "carton_undamaged": {
                    "type": "object",
                    "required": ["check_key", "verdict", "confidence"],
                    "properties": {
                        "check_key": {"type": "string", "enum": ["carton_undamaged"]},
                        "verdict": {"type": "string", "enum": ["PASS", "FAIL", "UNCERTAIN"]},
                        "expected_value": {"type": "string"},
                        "observed_value": {"type": "string"},
                        "confidence": {"type": "number"},
                        "details": {"type": "string"},
                        "timestamp": {"type": "string"},
                        "image_identifier": {"type": ["string", "null"]},
                        "bounding_box": {"type": ["object", "null"]}
                    }
                },
                "unit_undamaged": {
                    "type": "object",
                    "required": ["check_key", "verdict", "confidence"],
                    "properties": {
                        "check_key": {"type": "string", "enum": ["unit_undamaged"]},
                        "verdict": {"type": "string", "enum": ["PASS", "FAIL", "UNCERTAIN"]},
                        "expected_value": {"type": "string"},
                        "observed_value": {"type": "string"},
                        "confidence": {"type": "number"},
                        "details": {"type": "string"},
                        "timestamp": {"type": "string"},
                        "image_identifier": {"type": ["string", "null"]},
                        "bounding_box": {"type": ["object", "null"]}
                    }
                },
                "variant_correct": {
                    "type": "object",
                    "required": ["check_key", "verdict", "confidence"],
                    "properties": {
                        "check_key": {"type": "string", "enum": ["variant_correct"]},
                        "verdict": {"type": "string", "enum": ["PASS", "FAIL", "UNCERTAIN"]},
                        "expected_value": {"type": "string"},
                        "observed_value": {"type": "string"},
                        "confidence": {"type": "number"},
                        "details": {"type": "string"},
                        "timestamp": {"type": "string"},
                        "image_identifier": {"type": ["string", "null"]},
                        "bounding_box": {"type": ["object", "null"]}
                    }
                }
            }
        },
        "inspection_findings": {
            "type": "object",
            "required": [
                "identity_match",
                "quantity_received",
                "carton_damage",
                "unit_damage",
                "quality_flags"
            ],
            "properties": {
                "identity_match": {"type": "string", "enum": ["yes", "no", "uncertain"]},
                "quantity_received": {
                    "type": "object",
                    "required": ["cartons_received", "units_per_carton", "total_units"],
                    "properties": {
                        "cartons_received": {"type": "integer"},
                        "units_per_carton": {"type": "integer"},
                        "total_units": {"type": "integer"},
                        "discrepancy_delta": {"type": "integer"}
                    }
                },
                "carton_damage": {"type": "string", "enum": ["none", "crushing", "water", "tears", "uncertain"]},
                "unit_damage": {"type": "string", "enum": ["none", "crushing", "water", "tears", "uncertain"]},
                "quality_flags": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "verdict": {
            "type": "object",
            "required": ["overall_verdict", "checks_summary", "confidence_score"],
            "properties": {
                "overall_verdict": {"type": "string", "enum": ["PASS", "FAIL", "UNCERTAIN", "PENDING_REVIEW"]},
                "confidence_score": {"type": "number"},
                "checks_summary": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "check_name": {"type": "string"},
                            "verdict": {"type": "string", "enum": ["PASS", "FAIL", "UNCERTAIN"]},
                            "confidence": {"type": "number"},
                            "details": {"type": "string"}
                        }
                    }
                }
            }
        },
        "proof_of_receipt": {
            "type": "object",
            "required": ["photo_refs"],
            "properties": {
                "photo_refs": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "execution_metadata": {
            "type": "object",
            "properties": {
                "execution_mode": {"type": "string"},
                "model_name": {"type": "string"},
                "is_real_ai": {"type": "boolean"},
                "captured_at": {"type": "string"}
            }
        },
        "audit_overrides": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "overridden_at": {"type": "string"},
                    "operator_id": {"type": "string"},
                    "reason": {"type": "string"},
                    "original_verdict": {"type": "string"},
                    "new_verdict": {"type": "string"}
                }
            }
        }
    }
}

def generate_evidence_contract(record: Dict[str, Any], overrides: list = None) -> Dict[str, Any]:
    """
    Serializes a receiving record into the standard Cross-Pod Evidence Contract JSON.
    Aligns check keys to: identity_matches_po, quantity_matches_po, carton_undamaged,
    unit_undamaged, and variant_correct. Exposes subject.shipment_id and execution metadata.
    """
    q_flags_list = [f.strip() for f in record.get("quality_flags", "").split(";") if f.strip()]
    photos_list = [p.strip() for p in record.get("photo_refs", "").split(";") if p.strip()]
    
    qty_ord = int(record.get("qty_ordered", 0))
    qty_rec = int(record.get("qty_received", 0))

    # Parse raw evidence if available to recover bounding boxes or execution metadata
    raw_evidence = {}
    if record.get("evidence_data"):
        try:
            raw_evidence = json.loads(record["evidence_data"]) if isinstance(record["evidence_data"], str) else record["evidence_data"]
        except Exception:
            raw_evidence = {}

    primary_photo = photos_list[0] if photos_list else f"fixtures/receiving/{record['unit_id']}_pallet.jpg"
    captured_at = record.get("captured_at", datetime.utcnow().isoformat())
    shipment_id = record.get("shipment_id")

    # Extract bounding boxes from structured evidence if present (Priority 8)
    boxes_by_check = {}
    if isinstance(raw_evidence, dict) and "individual_checks" in raw_evidence:
        for chk in raw_evidence.get("individual_checks", []):
            if isinstance(chk, dict) and chk.get("bounding_box"):
                boxes_by_check[chk.get("check_name", "")] = chk.get("bounding_box")

    # Mapping internal check representations to agreed Cross-Pod Contract check keys (Priority 3)
    # 1. identity_matches_po (from identity_match: yes/no/uncertain)
    id_m = record.get("identity_match", "uncertain")
    id_verdict = "PASS" if id_m == "yes" else ("FAIL" if id_m == "no" else "UNCERTAIN")
    id_confidence = 0.95 if id_m == "yes" else (0.92 if id_m == "no" else 0.45)
    id_box = boxes_by_check.get("Product/SKU Identity") or boxes_by_check.get("Identity Match")

    # 2. quantity_matches_po (from qty_received vs qty_ordered)
    qty_verdict = "PASS" if qty_rec == qty_ord else "FAIL"
    qty_confidence = 0.99 if qty_rec == qty_ord else 0.95

    # 3. carton_undamaged (from carton_damage: none/crushing/water/tears/uncertain)
    c_dmg = record.get("carton_damage", "none")
    carton_verdict = "PASS" if c_dmg == "none" else ("UNCERTAIN" if c_dmg == "uncertain" else "FAIL")
    carton_confidence = 0.90 if c_dmg == "none" else 0.88
    carton_box = boxes_by_check.get("Carton Physical Integrity") or boxes_by_check.get("Carton Damage")

    # 4. unit_undamaged (from unit_damage: none/crushing/water/tears/uncertain)
    u_dmg = record.get("unit_damage", "none")
    unit_verdict = "PASS" if u_dmg == "none" else ("UNCERTAIN" if u_dmg == "uncertain" else "FAIL")
    unit_confidence = 0.88 if u_dmg == "none" else 0.85
    unit_box = boxes_by_check.get("Unit Physical Integrity") or boxes_by_check.get("Unit Damage")

    # 5. variant_correct (from quality_flags: spec/colour/variant mismatches)
    spec_failures = [f for f in q_flags_list if f in ["wrong_colour", "wrong_variant", "missing_components"]]
    variant_verdict = "FAIL" if spec_failures else "PASS"
    variant_confidence = 0.93

    cross_pod_checks = {
        "identity_matches_po": {
            "check_key": "identity_matches_po",
            "verdict": id_verdict,
            "expected_value": record.get("sku", ""),
            "observed_value": record.get("sku", "") if id_m == "yes" else "MISMATCH_OR_UNREADABLE",
            "confidence": id_confidence,
            "details": f"Goods identity match against PO line: {id_m}",
            "timestamp": captured_at,
            "image_identifier": primary_photo,
            "bounding_box": id_box
        },
        "quantity_matches_po": {
            "check_key": "quantity_matches_po",
            "verdict": qty_verdict,
            "expected_value": f"{qty_ord} units",
            "observed_value": f"{qty_rec} units",
            "confidence": qty_confidence,
            "details": f"Expected {qty_ord} units, counted {qty_rec} units (delta: {qty_rec - qty_ord})",
            "timestamp": captured_at,
            "image_identifier": primary_photo,
            "bounding_box": None
        },
        "carton_undamaged": {
            "check_key": "carton_undamaged",
            "verdict": carton_verdict,
            "expected_value": "none",
            "observed_value": c_dmg,
            "confidence": carton_confidence,
            "details": f"Carton physical integrity: {c_dmg}",
            "timestamp": captured_at,
            "image_identifier": primary_photo,
            "bounding_box": carton_box
        },
        "unit_undamaged": {
            "check_key": "unit_undamaged",
            "verdict": unit_verdict,
            "expected_value": "none",
            "observed_value": u_dmg,
            "confidence": unit_confidence,
            "details": f"Unit physical integrity: {u_dmg}",
            "timestamp": captured_at,
            "image_identifier": primary_photo,
            "bounding_box": unit_box
        },
        "variant_correct": {
            "check_key": "variant_correct",
            "verdict": variant_verdict,
            "expected_value": f"Spec: {record.get('spec_colour', '')} {record.get('spec_variant', '')}".strip(),
            "observed_value": "Matches spec" if variant_verdict == "PASS" else f"Flags: {', '.join(q_flags_list)}",
            "confidence": variant_confidence,
            "details": f"Quality flags: {', '.join(q_flags_list)}" if q_flags_list else "All specifications match agreed PO line",
            "timestamp": captured_at,
            "image_identifier": primary_photo,
            "bounding_box": None
        }
    }

    po_line_ref = {
        "po_number": record.get("po_number", ""),
        "po_line": int(record.get("po_line", 1)),
        "supplier": record.get("supplier", ""),
        "sku": record.get("sku", ""),
        "asin": record.get("asin", ""),
        "product_title": record.get("product_title", ""),
        "spec": {
            "colour": record.get("spec_colour", ""),
            "variant": record.get("spec_variant", ""),
            "components": record.get("spec_components", "")
        },
        "qty_ordered": qty_ord
    }

    subject_payload = {
        "unit_id": record["unit_id"],
        "shipment_id": shipment_id,
        "po_line_reference": po_line_ref
    }

    execution_metadata = {
        "execution_mode": raw_evidence.get("execution_mode", "DEMO_MODE_SYNTHETIC"),
        "model_name": raw_evidence.get("model_name", "Deterministic-Rule-Mock-Agent (Demo Mode)"),
        "is_real_ai": raw_evidence.get("is_real_ai", False),
        "captured_at": captured_at
    }

    evidence = {
        "schema_version": "1.0.0",
        "record_id": record["record_id"],
        "unit_id": record["unit_id"],
        "shipment_id": shipment_id,
        "org_id": record["org_id"],
        "stage": "01_RECEIVING",
        "captured_at": captured_at,
        "operator_id": record.get("operator_id", "op_default"),
        "subject": subject_payload,
        "po_line_reference": po_line_ref,
        "checks": cross_pod_checks,
        "inspection_findings": {
            "identity_match": id_m,
            "quantity_received": {
                "cartons_received": int(record.get("cartons_received", 0)),
                "units_per_carton": int(record.get("units_per_carton_counted", 0)),
                "total_units": qty_rec,
                "discrepancy_delta": qty_rec - qty_ord
            },
            "carton_damage": c_dmg,
            "unit_damage": u_dmg,
            "quality_flags": q_flags_list
        },
        "verdict": {
            "overall_verdict": record.get("overall_verdict", "UNCERTAIN"),
            "confidence_score": float(record.get("agent_confidence", 0.9)),
            "checks_summary": [
                {
                    "check_name": "Identity Match",
                    "verdict": id_verdict,
                    "confidence": id_confidence,
                    "details": f"Goods identity match: {id_m}"
                },
                {
                    "check_name": "Quantity Count",
                    "verdict": qty_verdict,
                    "confidence": qty_confidence,
                    "details": f"{qty_rec} counted vs {qty_ord} expected"
                },
                {
                    "check_name": "Carton Damage",
                    "verdict": carton_verdict,
                    "confidence": carton_confidence,
                    "details": f"Carton state: {c_dmg}"
                },
                {
                    "check_name": "Unit Damage",
                    "verdict": unit_verdict,
                    "confidence": unit_confidence,
                    "details": f"Unit state: {u_dmg}"
                },
                {
                    "check_name": "Spec Quality",
                    "verdict": variant_verdict,
                    "confidence": variant_confidence,
                    "details": f"Quality flags: {', '.join(q_flags_list)}" if q_flags_list else "All specs match"
                }
            ]
        },
        "proof_of_receipt": {
            "photo_refs": photos_list if photos_list else [
                f"fixtures/receiving/{record['unit_id']}_pallet.jpg",
                f"fixtures/receiving/{record['unit_id']}_carton.jpg",
                f"fixtures/receiving/{record['unit_id']}_unit.jpg"
            ]
        },
        "execution_metadata": execution_metadata,
        "audit_overrides": overrides or []
    }

    return evidence
