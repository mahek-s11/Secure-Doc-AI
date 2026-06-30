"""
=========================================================
Secure-Doc-AI
Report Builder
Purpose
This module assembles the reasoning and recommendation outputs
into a structured AI underwriting report. It produces both a
JSON-ready report object and an optional human-readable text
summary.
=========================================================
"""

import json
from datetime import datetime

from reasoning_engine import perform_reasoning
from recommendation_engine import generate_recommendation


# =====================================================
# Header Builder
# =====================================================

def build_header(application_id, documents_analyzed, created_at=None):
    return {
        "application_id": application_id,
        "documents_analyzed": documents_analyzed,
        "report_generated_at": created_at or datetime.utcnow().isoformat() + "Z",
        "report_version": "1.0",
    }


def build_metadata(created_at=None, analysis_status="Completed"):
    if created_at is None:
        generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(created_at, datetime):
        generated_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
    else:
        generated_at = str(created_at).replace("T", " ").replace("Z", "").split(".")[0]

    return {
        "system": "Secure-Doc-AI",
        "module": "AI Underwriting Assistant",
        "version": "1.0",
        "mode": "Offline",
        "generated_at": generated_at,
        "analysis_status": analysis_status,
    }


# =====================================================
# Executive Summary Builder
# =====================================================

def build_executive_summary(reasoning):
    return {
        "summary": reasoning.get("executive_summary", "A summary of the evidence is provided below."),
        "risk_narrative": reasoning.get("risk_narrative", "No narrative was generated."),
    }


# =====================================================
# Application Overview
# =====================================================

def build_application_overview(application_id, documents, risk_score=None, decision=None, name_validation=None):
    return {
        "application_id": application_id,
        "documents_submitted": documents,
        "risk_score": risk_score,
        "decision": decision,
        "identity_validation": name_validation,
    }


# =====================================================
# Risk Assessment Section
# =====================================================

def build_risk_assessment_section(reasoning):
    return {
        "overall_severity": reasoning.get("overall_severity"),
        "evidence_quality": reasoning.get("evidence_quality"),
        "patterns": reasoning.get("patterns", []),
        "contradictions": reasoning.get("contradictions", []),
    }


# =====================================================
# AI Findings Section
# =====================================================

def build_ai_findings_section(reasoning):
    return {
        "key_findings": reasoning.get("key_findings", []),
        "ranked_evidence": reasoning.get("ranked_evidence", []),
        "risk_indicators": reasoning.get("risk_indicators", []),
    }


# =====================================================
# Document Analysis Section
# =====================================================

def build_document_analysis_section(reasoning):
    analysis = reasoning.get("document_analysis", {})
    return {
        "affected_documents": analysis.get("affected_documents", []),
        "document_breakdown": analysis.get("document_breakdown", {}),
        "highest_risk_document": analysis.get("highest_risk_document"),
        "document_wise_analysis": reasoning.get("document_wise_analysis", {}),
    }


# =====================================================
# Identity Verification Section
# =====================================================

def build_identity_verification_section(reasoning):
    identity = reasoning.get("identity_analysis", {})
    return {
        "status": identity.get("status"),
        "summary": identity.get("summary"),
        "issues": identity.get("issues", []),
    }


# =====================================================
# Cross-Document Validation Section
# =====================================================

def build_cross_document_validation_section(reasoning):
    cross_document_findings = [item for item in reasoning.get("key_findings", []) if item.get("category") == "Cross Document Validation"]
    return {
        "cross_document_findings": cross_document_findings,
        "summary": "Cross-document inconsistencies are provided if detected.",
    }


# =====================================================
# Forgery Analysis Section
# =====================================================

def build_forgery_analysis_section(reasoning):
    fraud = reasoning.get("fraud_analysis", {})
    return {
        "fraud_signals": fraud.get("fraud_signals", []),
        "tampering_detected": fraud.get("tampering_detected", False),
        "fraud_probability": fraud.get("fraud_probability"),
        "risk_level": fraud.get("risk_level"),
    }


# =====================================================
# Evidence Strength Section
# =====================================================

def build_evidence_strength_section(reasoning):
    strength = reasoning.get("evidence_strength_analysis", {})
    return {
        "quality": strength.get("quality"),
        "confidence_score": strength.get("confidence"),
        "evidence_count": strength.get("evidence_count"),
        "strength": strength.get("strength"),
    }


# =====================================================
# Underwriting Reasoning Section
# =====================================================

def build_underwriting_reasoning_section(reasoning):
    underwriting = reasoning.get("underwriting_reasoning", {})
    return {
        "recommendation": underwriting.get("recommendation"),
        "review_focus": underwriting.get("review_focus", []),
        "next_steps": underwriting.get("next_steps", []),
    }


# =====================================================
# Business Impact Section
# =====================================================

def build_business_impact_section(reasoning):
    impact = reasoning.get("business_impact", {})
    return {
        "impact_level": impact.get("impact_level"),
        "summary": impact.get("summary"),
        "potential_consequences": impact.get("potential_consequences", []),
    }


# =====================================================
# Recommendation Section
# =====================================================

def build_recommendation_section(recommendation):
    return {
        "underwriting_decision": recommendation.get("underwriting_decision", {}),
        "manual_review": recommendation.get("manual_review", {}),
        "fraud_investigation_recommendation": recommendation.get("fraud_investigation_recommendation", {}),
        "compliance_recommendation": recommendation.get("compliance_recommendation"),
        "risk_mitigation": recommendation.get("risk_mitigation", []),
        "priority_level": recommendation.get("priority_level"),
        "sla_recommendation": recommendation.get("sla_recommendation"),
    }


# =====================================================
# Verification Checklist Section
# =====================================================

def build_verification_checklist_section(recommendation):
    return {
        "verification_checklist": recommendation.get("verification_checklist", []),
    }


# =====================================================
# Required Documents Section
# =====================================================

def build_required_documents_section(recommendation):
    return {
        "required_documents": recommendation.get("required_documents", []),
    }


# =====================================================
# Compliance Notes Section
# =====================================================

def build_compliance_notes_section(reasoning, recommendation):
    return {
        "notes": reasoning.get("compliance_notes", []),
        "recommendation": recommendation.get("compliance_recommendation"),
    }


# =====================================================
# Next Steps Section
# =====================================================

def build_next_steps_section(reasoning, recommendation):
    next_steps = reasoning.get("underwriting_reasoning", {}).get("next_steps", [])
    if not next_steps:
        next_steps = [recommendation.get("underwriting_decision", {}).get("summary", "Proceed according to underwriting guidance.")]
    return {
        "next_steps": next_steps,
    }


# =====================================================
# Timeline Section
# =====================================================

def build_timeline_section(recommendation):
    return {
        "priority_level": recommendation.get("priority_level"),
        "sla": recommendation.get("sla_recommendation"),
        "requested_at": datetime.utcnow().isoformat() + "Z",
    }


# =====================================================
# Final Decision Section
# =====================================================

def build_final_decision_section(recommendation):
    decision = recommendation.get("underwriting_decision", {})
    manual_review = recommendation.get("manual_review", {})
    return {
        "final_decision": decision.get("decision"),
        "risk_level": decision.get("risk_level"),
        "manual_review_required": manual_review.get("required", False),
        "decision_summary": decision.get("summary"),
        "processing_status": recommendation.get("processing_status"),
        "timeline": recommendation.get("timeline", {}),
        "escalation": recommendation.get("escalation", {}),
    }


# =====================================================
# JSON Report Generator
# =====================================================

def generate_json_report(report_object):
    return json.dumps(report_object, indent=4)


# =====================================================
# Text Report Generator (Optional)
# =====================================================

def _format_bullet_line(text):
    return f"• {text}"


def _format_check_line(text):
    return f"✓ {text}"


def _format_identity_status(status):
    if status is None:
        return "UNKNOWN"
    return "PASSED" if str(status).strip().upper() == "PASS" else "FAILED"


def _format_confidence_label(quality):
    mapping = {
        "Very Strong": "High",
        "Strong": "High",
        "Moderate": "Medium",
        "Weak": "Low",
        "Insufficient": "Low",
    }
    return mapping.get(str(quality), str(quality))


def _format_percentage(value):
    try:
        if value is None:
            return "Unknown"
        return f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return str(value)


def _format_underwriting_decision(decision):
    normalized = str(decision or "").strip().lower()
    if "manual" in normalized:
        return "MANUAL REVIEW"
    if "expanded" in normalized:
        return "EXPANDED VERIFICATION"
    if "standard" in normalized:
        return "STANDARD REVIEW"
    return decision or "UNKNOWN"


def _format_priority_level(priority):
    if not priority:
        return "UNKNOWN"
    text = str(priority).strip()
    if text.lower() == "immediate":
        return "CRITICAL"
    return text.upper()


def _build_default_next_steps(report):
    document_analysis = report.get("document_analysis", {}).get("affected_documents", [])
    steps = []
    if report.get("identity_verification", {}).get("status") == "FAIL":
        steps.append("Verify applicant identity")

    if document_analysis:
        steps.append("Authenticate submitted documents")

    if "Salary Slip" in document_analysis:
        steps.append("Review original salary slip")
    if "Bank Statement" in document_analysis:
        steps.append("Review bank statement")
    if "Property Document" in document_analysis:
        steps.append("Verify property ownership")

    if report.get("recommendation_section", {}).get("fraud_investigation_recommendation", {}).get("required"):
        steps.append("Escalate to fraud investigation")

    # Keep order consistent and remove duplicates
    ordered = []
    for step in [
        "Verify applicant identity",
        "Authenticate submitted documents",
        "Review original salary slip",
        "Review bank statement",
        "Verify property ownership",
        "Escalate to fraud investigation",
    ]:
        if step in steps and step not in ordered:
            ordered.append(step)

    return ordered


def generate_text_report(report):
    header = report.get("header", {})
    metadata = report.get("metadata", {})
    overview = report.get("application_overview", {})
    risk_assessment = report.get("risk_assessment", {})
    findings = report.get("ai_findings", {}).get("key_findings", [])
    recommendation_section = report.get("recommendation_section", {})
    next_steps = report.get("next_steps", {}).get("next_steps", [])
    document_analysis = report.get("document_analysis", {})
    final_decision = report.get("final_decision", {})

    if not next_steps or any(
        phrase in str(step).lower()
        for step in next_steps
        for phrase in ["manual review is required", "supporting documentation", "proceed according"]
    ):
        next_steps = _build_default_next_steps(report)

    lines = []
    lines.append("==================================================")
    lines.append("SECURE-DOC-AI")
    lines.append("AI UNDERWRITING ASSISTANT REPORT")
    lines.append("==================================================")
    lines.append("")
    lines.append(f"Application ID : {overview.get('application_id', header.get('application_id', 'Unknown'))}")
    lines.append(f"Documents      : {overview.get('documents_submitted', header.get('documents_analyzed', 0))}")
    lines.append("")
    lines.append("--------------------------------------------------")
    lines.append("REPORT METADATA")
    lines.append("--------------------------------------------------")
    lines.append(f"System         : {metadata.get('system', 'Secure-Doc-AI')}")
    lines.append(f"Module         : {metadata.get('module', 'AI Underwriting Assistant')}")
    lines.append(f"Version        : {metadata.get('version', '1.0')}")
    lines.append(f"Mode           : {metadata.get('mode', 'Offline')}")
    lines.append(f"Generated At   : {metadata.get('generated_at', 'Unknown')}")
    lines.append(f"Analysis Status: {metadata.get('analysis_status', 'Completed')}")
    lines.append("")
    lines.append("--------------------------------------------------")
    lines.append("EXECUTIVE SUMMARY")
    lines.append("--------------------------------------------------")
    lines.append(report.get('executive_summary', {}).get('summary', 'No executive summary available.'))
    lines.append("")
    lines.append("--------------------------------------------------")
    lines.append("RISK ASSESSMENT")
    lines.append("--------------------------------------------------")
    lines.append(f"Risk Score        : {overview.get('risk_score', 'N/A')}")
    lines.append(f"Risk Level        : {overview.get('decision', 'UNKNOWN')}")
    lines.append(f"AI Confidence     : {_format_percentage(report.get('evidence_strength', {}).get('confidence_score'))}")
    lines.append(f"Identity Status   : {_format_identity_status(overview.get('identity_validation'))}")
    lines.append("")
    lines.append("--------------------------------------------------")
    lines.append("KEY FINDINGS")
    lines.append("--------------------------------------------------")
    if findings:
        for finding in findings:
            lines.append(_format_bullet_line(finding.get('finding', 'Unknown finding')))
    else:
        ranked_evidence = report.get('ai_findings', {}).get('ranked_evidence', [])
        for item in ranked_evidence:
            lines.append(_format_bullet_line(item.get('finding', 'Unknown finding')))
    lines.append("")
    lines.append("--------------------------------------------------")
    lines.append("DOCUMENT ANALYSIS")
    lines.append("--------------------------------------------------")
    lines.append(f"Affected Documents : {', '.join(document_analysis.get('affected_documents', [])) if document_analysis.get('affected_documents') else 'None'}")
    lines.append(f"Highest Risk Document : {document_analysis.get('highest_risk_document', 'Unknown')}")
    for document_name, details in document_analysis.get('document_wise_analysis', {}).items():
        lines.append(f"{document_name} : {details.get('highest_severity', 'Low')} ({details.get('evidence_count', 0)} finding(s))")
    lines.append("")
    lines.append("--------------------------------------------------")
    lines.append("BUSINESS IMPACT")
    lines.append("--------------------------------------------------")
    business_impact = report.get('business_impact', {})
    lines.append(business_impact.get('summary', 'No business impact summary available.'))
    for consequence in business_impact.get('potential_consequences', []):
        lines.append(_format_bullet_line(consequence))
    lines.append("")
    lines.append("--------------------------------------------------")
    lines.append("COMPLIANCE NOTES")
    lines.append("--------------------------------------------------")
    compliance_notes = report.get('compliance_notes', {})
    for note in compliance_notes.get('notes', []):
        lines.append(_format_bullet_line(note))
    if compliance_notes.get('recommendation'):
        lines.append(_format_bullet_line(compliance_notes.get('recommendation')))
    lines.append("")
    lines.append("--------------------------------------------------")
    lines.append("VERIFICATION CHECKLIST")
    lines.append("--------------------------------------------------")
    for item in report.get('verification_checklist', {}).get('verification_checklist', []):
        lines.append(_format_check_line(item))
    if not report.get('verification_checklist', {}).get('verification_checklist'):
        lines.append(_format_check_line('No checklist items available.'))
    lines.append("")
    lines.append("--------------------------------------------------")
    lines.append("REQUIRED DOCUMENTS")
    lines.append("--------------------------------------------------")
    for doc in report.get('required_documents', {}).get('required_documents', []):
        lines.append(_format_bullet_line(doc))
    if not report.get('required_documents', {}).get('required_documents'):
        lines.append(_format_bullet_line('None specified.'))
    lines.append("")
    lines.append("--------------------------------------------------")
    lines.append("UNDERWRITING RECOMMENDATION")
    lines.append("--------------------------------------------------")
    underwriting = recommendation_section.get('underwriting_decision', {})
    lines.append(f"Decision          : {_format_underwriting_decision(underwriting.get('decision', 'UNKNOWN'))}")
    lines.append(f"Priority          : {_format_priority_level(recommendation_section.get('priority_level', 'UNKNOWN'))}")
    lines.append(f"Processing Status : {final_decision.get('processing_status', 'Standard processing')}")
    lines.append("")
    lines.append("--------------------------------------------------")
    lines.append("NEXT STEPS")
    lines.append("--------------------------------------------------")
    if next_steps:
        for step in next_steps:
            lines.append(_format_check_line(step))
    else:
        lines.append(_format_check_line("No next steps available."))
    lines.append("")
    lines.append("--------------------------------------------------")
    lines.append("FINAL DECISION")
    lines.append("--------------------------------------------------")
    lines.append(f"Outcome : {final_decision.get('final_decision', 'Unknown')}")
    lines.append(f"Reason  : {final_decision.get('decision_summary', 'No decision summary available.')}")
    lines.append(f"Timeline: {final_decision.get('timeline', {}).get('sla', 'Standard review')}")
    lines.append("")
    lines.append("==================================================")
    lines.append("Prepared by Secure-Doc-AI Offline Underwriting Assistant")
    lines.append("This report supports manual review and does not replace human judgment.")
    lines.append("==================================================")
    return "\n".join(lines)


# =====================================================
# Build Report
# =====================================================

def build_report(application_id, evidence, documents_analyzed=None, risk_score=None, decision=None, name_validation=None):
    reasoning = perform_reasoning(evidence)
    recommendation = generate_recommendation(evidence)

    header = build_header(application_id, documents_analyzed or len(reasoning.get('documents', [])))
    metadata = build_metadata(created_at=header.get('report_generated_at'))
    overview = build_application_overview(application_id, documents_analyzed or len(reasoning.get('documents', [])), risk_score, decision, name_validation)
    executive_summary = build_executive_summary(reasoning)
    risk_assessment = build_risk_assessment_section(reasoning)
    ai_findings = build_ai_findings_section(reasoning)
    document_analysis = build_document_analysis_section(reasoning)
    identity_verification = build_identity_verification_section(reasoning)
    cross_document_validation = build_cross_document_validation_section(reasoning)
    forgery_analysis = build_forgery_analysis_section(reasoning)
    evidence_strength = build_evidence_strength_section(reasoning)
    underwriting_reasoning = build_underwriting_reasoning_section(reasoning)
    business_impact = build_business_impact_section(reasoning)
    recommendation_section = build_recommendation_section(recommendation)
    verification_checklist = build_verification_checklist_section(recommendation)
    required_documents = build_required_documents_section(recommendation)
    compliance_notes = build_compliance_notes_section(reasoning, recommendation)
    next_steps = build_next_steps_section(reasoning, recommendation)
    timeline = build_timeline_section(recommendation)
    final_decision = build_final_decision_section(recommendation)

    report = {
        "header": header,
        "metadata": metadata,
        "executive_summary": executive_summary,
        "application_overview": overview,
        "risk_assessment": risk_assessment,
        "ai_findings": ai_findings,
        "document_analysis": document_analysis,
        "identity_verification": identity_verification,
        "cross_document_validation": cross_document_validation,
        "forgery_analysis": forgery_analysis,
        "evidence_strength": evidence_strength,
        "underwriting_reasoning": underwriting_reasoning,
        "business_impact": business_impact,
        "recommendation_section": recommendation_section,
        "verification_checklist": verification_checklist,
        "required_documents": required_documents,
        "compliance_notes": compliance_notes,
        "next_steps": next_steps,
        "timeline": timeline,
        "final_decision": final_decision,
    }

    report["text_summary"] = generate_text_report(report)
    return report


# =====================================================
# Example Execution
# =====================================================
if __name__ == "__main__":
    sample_evidence = [
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

    report = build_report(
        application_id="sample_001",
        evidence=sample_evidence,
        documents_analyzed=2,
        risk_score=230,
        decision="HIGH RISK",
        name_validation="FAIL",
    )
    print(generate_json_report(report))
