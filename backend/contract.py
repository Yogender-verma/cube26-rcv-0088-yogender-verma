"""
Cross-Pod Evidence Contract Generator (Receiving Manager -> Prep & Recovery Managers)
Standardized schema specification and serializer for Step 01 Receiving output.
"""

from typing import Dict, Any
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
        "po_line_reference",
        "inspection_findings",
        "verdict",
        "proof_of_receipt"
    ],
    "properties": {
        "schema_version": {"type": "string", "enum": ["1.0.0"]},
        "record_id": {"type": "string"},
        "unit_id": {"type": "string"},
        "org_id": {"type": "string"},
        "stage": {"type": "string", "enum": ["01_RECEIVING"]},
        "captured_at": {"type": "string"},
        "operator_id": {"type": "string"},
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
    """Serializes a receiving record into the standard Cross-Pod Evidence Contract JSON."""
    q_flags_list = [f.strip() for f in record.get("quality_flags", "").split(";") if f.strip()]
    photos_list = [p.strip() for p in record.get("photo_refs", "").split(";") if p.strip()]
    
    qty_ord = int(record.get("qty_ordered", 0))
    qty_rec = int(record.get("qty_received", 0))

    evidence = {
        "schema_version": "1.0.0",
        "record_id": record["record_id"],
        "unit_id": record["unit_id"],
        "org_id": record["org_id"],
        "stage": "01_RECEIVING",
        "captured_at": record.get("captured_at", datetime.utcnow().isoformat()),
        "operator_id": record.get("operator_id", "op_default"),
        "po_line_reference": {
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
        },
        "inspection_findings": {
            "identity_match": record.get("identity_match", "uncertain"),
            "quantity_received": {
                "cartons_received": int(record.get("cartons_received", 0)),
                "units_per_carton": int(record.get("units_per_carton_counted", 0)),
                "total_units": qty_rec,
                "discrepancy_delta": qty_rec - qty_ord
            },
            "carton_damage": record.get("carton_damage", "none"),
            "unit_damage": record.get("unit_damage", "none"),
            "quality_flags": q_flags_list
        },
        "verdict": {
            "overall_verdict": record.get("overall_verdict", "UNCERTAIN"),
            "confidence_score": float(record.get("agent_confidence", 0.9)),
            "checks_summary": [
                {
                    "check_name": "Identity Match",
                    "verdict": "PASS" if record.get("identity_match") == "yes" else ("FAIL" if record.get("identity_match") == "no" else "UNCERTAIN"),
                    "confidence": 0.95 if record.get("identity_match") == "yes" else 0.45,
                    "details": f"Goods identity match: {record.get('identity_match')}"
                },
                {
                    "check_name": "Quantity Count",
                    "verdict": "PASS" if qty_rec == qty_ord else "FAIL",
                    "confidence": 0.99,
                    "details": f"{qty_rec} counted vs {qty_ord} expected"
                },
                {
                    "check_name": "Carton Damage",
                    "verdict": "PASS" if record.get("carton_damage") == "none" else ("UNCERTAIN" if record.get("carton_damage") == "uncertain" else "FAIL"),
                    "confidence": 0.90,
                    "details": f"Carton state: {record.get('carton_damage')}"
                },
                {
                    "check_name": "Unit Damage",
                    "verdict": "PASS" if record.get("unit_damage") == "none" else ("UNCERTAIN" if record.get("unit_damage") == "uncertain" else "FAIL"),
                    "confidence": 0.88,
                    "details": f"Unit state: {record.get('unit_damage')}"
                },
                {
                    "check_name": "Spec Quality",
                    "verdict": "PASS" if not q_flags_list else "FAIL",
                    "confidence": 0.93,
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
        "audit_overrides": overrides or []
    }

    return evidence
