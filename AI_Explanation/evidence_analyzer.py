"""
=========================================================
Secure-Doc-AI
Evidence Analyzer
Purpose
Converts raw Risk Engine reasons into structured evidence
used by the AI Underwriting Assistant.
No AI model is used.
This module behaves like an Explainable AI (XAI)
reasoning engine.
=========================================================
"""

import re
# -------------------------------------------------------
# Severity Mapping
# -------------------------------------------------------

SEVERITY_MAP = {
    "critical": 5,
    "high": 4,
    "medium": 3,
    "low": 2,
    "info": 1
}


# -------------------------------------------------------
# Detect document name
# -------------------------------------------------------

def detect_document(reason: str):

    text = reason.lower()

    if "salary" in text:
        return "Salary Slip"

    if "bank" in text:
        return "Bank Statement"

    if "property" in text:
        return "Property Document"

    if "mismatch" in text or "cross-document" in text or "cross document" in text:
        return "Cross Document Validation"

    if "name" in text or "identity" in text or "inconsistent" in text:
        return "Identity Verification"

    if "metadata" in text:
        return "Metadata Analysis"

    return "General Verification"


# -------------------------------------------------------
# Detect category
# -------------------------------------------------------

def detect_category(reason: str):

    text = reason.lower()

    if "forgery" in text:
        return "Forgery Detection"

    if "tampering" in text:
        return "Document Tampering"

    if "metadata" in text:
        return "Metadata Analysis"

    if "mismatch" in text:
        return "Cross Document Validation"

    if "name" in text:
        return "Identity Verification"

    return "General Verification"


# -------------------------------------------------------
# Detect severity
# -------------------------------------------------------

def detect_severity(reason: str):

    text = reason.lower()

    if "tampering" in text:
        return "Critical"

    if "forgery" in text:
        return "Critical"

    if "metadata" in text:
        return "High"

    if "mismatch" in text:
        return "High"

    if "missing" in text:
        return "Medium"

    return "Low"


# -------------------------------------------------------
# Confidence estimation
# -------------------------------------------------------

def estimate_confidence(reason: str):

    severity = detect_severity(reason)

    mapping = {
        "Critical": 98,
        "High": 90,
        "Medium": 75,
        "Low": 60
    }

    return mapping.get(severity, 50)


# -------------------------------------------------------
# Build evidence object
# -------------------------------------------------------

def build_evidence(reason):

    evidence = {

        "raw_reason": reason,

        "document": detect_document(reason),

        "category": detect_category(reason),

        "severity": detect_severity(reason),

        "confidence": estimate_confidence(reason)

    }

    return evidence


# -------------------------------------------------------
# Analyse all reasons
# -------------------------------------------------------

def analyze_reasons(reasons):

    evidence = []

    for reason in reasons:

        evidence.append(build_evidence(reason))

    return evidence


# -------------------------------------------------------
# Count severity
# -------------------------------------------------------

def severity_statistics(evidence):

    stats = {

        "Critical": 0,

        "High": 0,

        "Medium": 0,

        "Low": 0

    }

    for item in evidence:

        level = item["severity"]

        stats[level] += 1

    return stats


# -------------------------------------------------------
# Category statistics
# -------------------------------------------------------

def category_statistics(evidence):

    result = {}

    for item in evidence:

        category = item["category"]

        result[category] = result.get(category, 0) + 1

    return result


# -------------------------------------------------------
# Document statistics
# -------------------------------------------------------

def document_statistics(evidence):

    result = {}

    for item in evidence:

        doc = item["document"]

        result[doc] = result.get(doc, 0) + 1

    return result


# -------------------------------------------------------
# Overall AI confidence
# -------------------------------------------------------

def overall_confidence(evidence):

    if len(evidence) == 0:
        return 50

    total = 0

    for item in evidence:
        total += item["confidence"]

    return round(total / len(evidence), 2)


# -------------------------------------------------------
# Fraud likelihood
# -------------------------------------------------------

def fraud_likelihood(evidence):

    score = 0

    for item in evidence:

        if item["severity"] == "Critical":
            score += 30

        elif item["severity"] == "High":
            score += 20

        elif item["severity"] == "Medium":
            score += 10

        else:
            score += 5

    return min(score, 100)


# -------------------------------------------------------
# Main analysis
# -------------------------------------------------------

def analyze_evidence(reasons):

    evidence = analyze_reasons(reasons)

    return {

        "evidence": evidence,

        "severity_statistics": severity_statistics(evidence),

        "category_statistics": category_statistics(evidence),

        "document_statistics": document_statistics(evidence),

        "overall_confidence": overall_confidence(evidence),

        "fraud_probability": fraud_likelihood(evidence)

    }


# -------------------------------------------------------
# Testing
# -------------------------------------------------------

if __name__ == "__main__":

    reasons = [

        "High forgery score in salary_slip",

        "Tampering detected in salary_slip",

        "High forgery score in bank_statement",

        "Tampering detected in property_document",

        "Name mismatch across documents"

    ]

    result = analyze_evidence(reasons)

    from pprint import pprint

    pprint(result)