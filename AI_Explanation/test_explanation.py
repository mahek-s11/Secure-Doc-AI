import json
from pathlib import Path

from explanation import generate_ai_explanation, load_risk_report


def run_case(case_name, payload):
    report = generate_ai_explanation(payload)
    assert report["application_id"] == payload["application_id"]
    assert "reasoning" in report
    assert "recommendation_engine" in report
    assert "text_report" in report
    assert "SECURE-DOC-AI" in report["text_report"]
    assert "EXECUTIVE SUMMARY" in report["text_report"]
    assert "DOCUMENT ANALYSIS" in report["text_report"]
    assert "FINAL DECISION" in report["text_report"]
    assert report["report"].get("metadata", {}).get("system") == "Secure-Doc-AI"
    assert report["report"].get("metadata", {}).get("module") == "AI Underwriting Assistant"
    assert report["report"].get("metadata", {}).get("analysis_status") == "Completed"
    return report


def print_complete_report(ai_report):
    text_report = ai_report.get("text_report", "")
    safe_text = text_report.encode("ascii", "replace").decode("ascii")
    print(safe_text)
    print("\n" + "=" * 80 + "\n")


def run_sample_report_test(sample_report_path):
    risk_data = load_risk_report(sample_report_path)

    if isinstance(risk_data, list):
        for report in risk_data:
            ai_report = generate_ai_explanation(report)
            print_complete_report(ai_report)
    else:
        ai_report = generate_ai_explanation(risk_data)
        print_complete_report(ai_report)


def run_all_scenarios():
    cases = [
        (
            "genuine_documents",
            {
                "application_id": "genuine_001",
                "documents": 3,
                "name_validation": "PASS",
                "risk_score": 0,
                "decision": "LOW RISK",
                "reasons": ["No suspicious activity detected"],
            },
        ),
        (
            "salary_slip_tampered",
            {
                "application_id": "tampered_salary_001",
                "documents": 3,
                "name_validation": "FAIL",
                "risk_score": 180,
                "decision": "HIGH RISK",
                "reasons": [
                    "High forgery score in salary_slip",
                    "Tampering detected in salary_slip",
                ],
            },
        ),
        (
            "bank_statement_tampered",
            {
                "application_id": "tampered_bank_001",
                "documents": 3,
                "name_validation": "FAIL",
                "risk_score": 190,
                "decision": "HIGH RISK",
                "reasons": [
                    "High forgery score in bank_statement",
                    "Tampering detected in bank_statement",
                ],
            },
        ),
        (
            "property_tampered",
            {
                "application_id": "tampered_property_001",
                "documents": 3,
                "name_validation": "FAIL",
                "risk_score": 200,
                "decision": "HIGH RISK",
                "reasons": [
                    "High forgery score in property_document",
                    "Tampering detected in property_document",
                ],
            },
        ),
        (
            "name_mismatch",
            {
                "application_id": "name_mismatch_001",
                "documents": 3,
                "name_validation": "FAIL",
                "risk_score": 120,
                "decision": "MEDIUM RISK",
                "reasons": ["Name mismatch across documents"],
            },
        ),
        (
            "low_risk",
            {
                "application_id": "low_risk_001",
                "documents": 3,
                "name_validation": "PASS",
                "risk_score": 10,
                "decision": "LOW RISK",
                "reasons": ["No suspicious activity detected"],
            },
        ),
        (
            "medium_risk",
            {
                "application_id": "medium_risk_001",
                "documents": 3,
                "name_validation": "PASS",
                "risk_score": 80,
                "decision": "MEDIUM RISK",
                "reasons": ["Minor inconsistencies detected"],
            },
        ),
        (
            "high_risk",
            {
                "application_id": "high_risk_001",
                "documents": 3,
                "name_validation": "FAIL",
                "risk_score": 235,
                "decision": "HIGH RISK",
                "reasons": [
                    "High forgery score in salary_slip",
                    "Tampering detected in salary_slip",
                    "High forgery score in bank_statement",
                    "Tampering detected in property_document",
                    "Name mismatch across documents",
                ],
            },
        ),
    ]

    for case_name, payload in cases:
        run_case(case_name, payload)

    print(f"AI explanation integration test passed for {len(cases)} scenarios.")


if __name__ == "__main__":
    sample_report_path = (
        Path(__file__).resolve().parent.parent
        / "Risk_Engine"
        / "reports"
        / "risk_report.json"
    )
    run_sample_report_test(sample_report_path)
    run_all_scenarios()
