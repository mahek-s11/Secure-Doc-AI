"""
=========================================================
Secure-Doc-AI
Recommendation Engine
Purpose
This module produces a structured underwriting recommendation
from normalized evidence. It focuses on recommendation rules,
manual review prioritization, fraud investigation guidance,
and compliance-driven next steps.
=========================================================
"""

from collections import Counter
from statistics import mean


# =====================================================
# Recommendation Rules
# =====================================================

SEVERITY_PRIORITY = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1,
}


DOCUMENT_RECOMMENDATIONS = {
    "Bank Statement": [
        "Verify transaction history consistency.",
        "Confirm bank account ownership with an independent source.",
    ],
    "Salary Slip": [
        "Validate employer details and payment dates.",
        "Cross-check salary slip totals against expected income.",
    ],
    "Property Document": [
        "Confirm property ownership records.",
        "Verify property valuation and submission date.",
    ],
    "Unknown Document": [
        "Review the item manually for relevance and authenticity.",
    ],
}


# =====================================================
# Utility helpers
# =====================================================

def _infer_severity(reason):
    text = str(reason or "").lower()
    if "tampering" in text or "forgery" in text:
        return "Critical"
    if "mismatch" in text or "metadata" in text:
        return "High"
    if "missing" in text:
        return "Medium"
    return "Low"


def normalize_evidence(evidence):
    if evidence is None:
        return []

    if isinstance(evidence, dict):
        if isinstance(evidence.get("evidence"), list):
            evidence = evidence["evidence"]
        elif isinstance(evidence.get("reasons"), list):
            evidence = evidence["reasons"]
        else:
            evidence = [evidence]

    if isinstance(evidence, str):
        evidence = [{"raw_reason": evidence}]

    if not isinstance(evidence, list):
        return []

    normalized = []
    for item in evidence:
        if isinstance(item, dict):
            raw_reason = item.get("raw_reason") or item.get("reason") or ""
            severity = item.get("severity") or _infer_severity(raw_reason)
            normalized.append({
                "raw_reason": raw_reason,
                "document": item.get("document", "Unknown Document"),
                "category": item.get("category", "General Verification"),
                "severity": severity,
                "confidence": item.get("confidence", 60),
            })
        elif isinstance(item, str):
            normalized.append({
                "raw_reason": item,
                "document": "Unknown Document",
                "category": "General Verification",
                "severity": _infer_severity(item),
                "confidence": 60,
            })
    return normalized


def count_severity_levels(evidence):
    levels = Counter()
    for item in evidence:
        levels[item.get("severity", "Low")] += 1
    return levels


def average_confidence(evidence):
    if not evidence:
        return 0
    values = [item.get("confidence", 0) for item in evidence]
    return round(mean(values), 2)


def determine_risk_level(evidence):
    if not evidence:
        return "Low"
    score = 0
    for item in evidence:
        score += SEVERITY_PRIORITY.get(item.get("severity"), 1)
    avg = score / len(evidence)
    if avg >= 3.5:
        return "Critical"
    if avg >= 2.7:
        return "High"
    if avg >= 1.8:
        return "Medium"
    return "Low"


# =====================================================
# Underwriting Decision
# =====================================================

def build_underwriting_decision(evidence):
    risk_level = determine_risk_level(evidence)
    if risk_level in ["Critical", "High"]:
        decision = "Require manual underwriting review"
    elif risk_level == "Medium":
        decision = "Require expanded verification"
    else:
        decision = "Proceed with standard underwriting"

    return {
        "risk_level": risk_level,
        "decision": decision,
        "summary": f"Underwriting recommendation based on {risk_level} risk evidence.",
    }


# =====================================================
# Manual Review Logic
# =====================================================

def evaluate_manual_review(evidence):
    risk_level = determine_risk_level(evidence)
    severity_counts = count_severity_levels(evidence)
    if risk_level == "Critical" or severity_counts["Critical"] >= 1:
        return {
            "required": True,
            "reason": "Critical evidence exists and manual review is required to protect against fraud.",
            "triggers": ["Critical severity finding", "Multiple high-risk indicators"],
        }

    if severity_counts["High"] >= 2 or severity_counts["Medium"] >= 3:
        return {
            "required": True,
            "reason": "Multiple elevated risk indicators were found, so manual review is advised.",
            "triggers": ["Multiple High severity items", "Multiple Medium severity items"],
        }

    return {
        "required": False,
        "reason": "The evidence does not currently require manual underwriting review.",
        "triggers": [],
    }


# =====================================================
# Verification Checklist
# =====================================================

def build_verification_checklist(evidence):
    checklist = [
        "Confirm applicant identity across all documents.",
        "Evaluate authenticity of each document type.",
        "Verify timestamps and submission dates.",
    ]

    documents = [item.get("document", "Unknown Document") for item in evidence]
    if "Bank Statement" in documents:
        checklist.append("Confirm bank statement payment history matches declared income.")
    if "Salary Slip" in documents:
        checklist.append("Validate salary slip employer details and pay period.")
    if "Property Document" in documents:
        checklist.append("Confirm property ownership and registration details.")

    return checklist


# =====================================================
# Required Documents
# =====================================================

def build_required_documents(evidence):
    required = set()
    if any(item.get("document") == "Salary Slip" for item in evidence):
        required.add("Employer verification letter")
    if any(item.get("document") == "Bank Statement" for item in evidence):
        required.add("Bank account statement from the last 3 months")
    if any(item.get("document") == "Property Document" for item in evidence):
        required.add("Title deed or property ownership certificate")

    if not required:
        required.add("Photo ID and proof of address")

    return list(required)


# =====================================================
# Banking Recommendations
# =====================================================

def build_banking_recommendations(evidence):
    recommendations = []
    if any(item.get("document") == "Bank Statement" for item in evidence):
        recommendations.append("Validate bank account ownership and transaction consistency.")
        recommendations.append("Confirm transaction amounts align with reported cash flow.")
    if not recommendations:
        recommendations.append("No specific banking recommendations available for the evidence supplied.")
    return recommendations


# =====================================================
# Fraud Investigation Recommendation
# =====================================================

def build_fraud_investigation_recommendation(evidence):
    risk_level = determine_risk_level(evidence)
    if risk_level == "Critical":
        return {
            "required": True,
            "reason": "Critical fraud indicators are present and should be escalated to the fraud investigation team.",
            "action": "Initiate fraud investigation immediately.",
        }
    if risk_level == "High":
        return {
            "required": True,
            "reason": "Significant anomalies exist and a targeted fraud review is recommended.",
            "action": "Refer case to fraud investigation for further analysis.",
        }
    return {
        "required": False,
        "reason": "No immediate fraud investigation is required based on the current evidence.",
        "action": "Monitor the case and revisit if additional evidence emerges.",
    }


# =====================================================
# Compliance Recommendation
# =====================================================

def build_compliance_recommendation(evidence):
    risk_level = determine_risk_level(evidence)
    if risk_level in ["Critical", "High"]:
        return "Escalate to compliance for regulatory and anti-fraud review."
    if risk_level == "Medium":
        return "Document the findings and keep the case under enhanced compliance oversight."
    return "Standard compliance controls are sufficient for this case."


# =====================================================
# Risk Mitigation
# =====================================================

def build_risk_mitigation(evidence):
    mitigation = []
    if determine_risk_level(evidence) in ["Critical", "High"]:
        mitigation.extend([
            "Suspend processing until manual verification is complete.",
            "Require independent proof of document authenticity.",
        ])
    else:
        mitigation.append("Apply standard verification controls and continue monitoring.")

    if any(item.get("category") == "Identity Verification" for item in evidence):
        mitigation.append("Retake identity verification checks for the applicant.")
    return mitigation


# =====================================================
# Priority Level
# =====================================================

def determine_priority_level(evidence):
    risk_level = determine_risk_level(evidence)
    if risk_level == "Critical":
        return "Immediate"
    if risk_level == "High":
        return "High"
    if risk_level == "Medium":
        return "Medium"
    return "Low"


# =====================================================
# SLA Recommendation
# =====================================================

def build_sla_recommendation(evidence):
    level = determine_priority_level(evidence)
    if level == "Immediate":
        return "Resolve within 2 business hours with senior review."
    if level == "High":
        return "Resolve within 1 business day with compliance involvement."
    if level == "Medium":
        return "Resolve within 2-3 business days with enhanced verification."
    return "Resolve within 5 business days under normal review."


def build_timeline(evidence):
    return {
        "priority": determine_priority_level(evidence),
        "sla": build_sla_recommendation(evidence),
        "status": "Priority handling" if determine_priority_level(evidence) in ["Immediate", "High"] else "Routine handling",
    }


def build_escalation(evidence):
    if determine_risk_level(evidence) in ["Critical", "High"]:
        return {
            "required": True,
            "target_team": "Fraud Investigation and Compliance",
            "reason": "Elevated fraud or identity risk requires senior review.",
        }
    return {
        "required": False,
        "target_team": "Standard Underwriting",
        "reason": "No escalation required at this stage.",
    }


def build_processing_status(evidence):
    risk_level = determine_risk_level(evidence)
    if risk_level == "Critical":
        return "Hold - Manual review pending"
    if risk_level == "High":
        return "Enhanced review"
    if risk_level == "Medium":
        return "Additional verification required"
    return "Standard processing"


# =====================================================
# Final Recommendation Object
# =====================================================

def build_final_recommendation_object(evidence):
    underwriting = build_underwriting_decision(evidence)
    manual_review = evaluate_manual_review(evidence)
    fraud_investigation = build_fraud_investigation_recommendation(evidence)

    return {
        "underwriting_decision": underwriting,
        "manual_review": manual_review,
        "verification_checklist": build_verification_checklist(evidence),
        "required_documents": build_required_documents(evidence),
        "banking_recommendations": build_banking_recommendations(evidence),
        "fraud_investigation_recommendation": fraud_investigation,
        "compliance_recommendation": build_compliance_recommendation(evidence),
        "risk_mitigation": build_risk_mitigation(evidence),
        "priority_level": determine_priority_level(evidence),
        "sla_recommendation": build_sla_recommendation(evidence),
        "timeline": build_timeline(evidence),
        "escalation": build_escalation(evidence),
        "processing_status": build_processing_status(evidence),
    }


# =====================================================
# Main Recommendation API
# =====================================================

def generate_recommendation(evidence):
    normalized = normalize_evidence(evidence)
    return build_final_recommendation_object(normalized)


# =====================================================
# Example execution
# =====================================================
if __name__ == "__main__":
    sample_reasons = [
        {
            "raw_reason": "High forgery score in salary_slip",
            "document": "Salary Slip",
            "category": "Forgery Detection",
            "severity": "Critical",
            "confidence": 98,
        },
        {
            "raw_reason": "Name mismatch across documents",
            "document": "Bank Statement",
            "category": "Identity Verification",
            "severity": "High",
            "confidence": 90,
        },
    ]
    recommendation = generate_recommendation(sample_reasons)
    print(recommendation)
