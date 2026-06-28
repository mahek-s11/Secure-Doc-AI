# Secure-Doc-AI

## AI-Powered Document Forgery Detection & Risk Assessment System

SecureDocAI is an AI-driven document verification system developed for the **Canara Bank Suraksha Cyber Hackathon**. It helps financial institutions detect forged or tampered documents, validate information across multiple documents, and generate an overall fraud risk assessment for loan and underwriting applications.

---

## Project Overview

Financial institutions receive thousands of documents such as salary slips, bank statements, and property documents every day. Manual verification is time-consuming and prone to human error.

SecureDocAI automates this verification process using Artificial Intelligence by:

* Extracting information from uploaded documents.
* Detecting document tampering and forgery.
* Performing cross-document validation.
* Calculating fraud risk scores.
* Generating explainable risk reports for decision-making.

---

## Features

### OCR-Based Data Extraction

* Extracts structured information from uploaded documents.
* Supports multiple document types.
* Calculates OCR confidence scores.

### Document Forgery Detection

* Detects signs of tampering.
* Assigns forgery confidence scores.
* Identifies suspicious modifications.

### Cross-Document Validation

* Compares applicant information across documents.
* Detects name mismatches.
* Validates document consistency.

### Intelligent Risk Engine

* Merges OCR and forgery detection outputs.
* Computes overall application risk.
* Classifies applications as:

  * Low Risk
  * Medium Risk
  * High Risk

### Risk Report Generation

* Produces structured JSON reports.
* Lists detected issues and reasons.
* Ready for dashboard visualization.

---

## Project Structure

```text
SecureDocAI/
│
├── OCR_Module/
│   ├── ocr.py
│   └── output/
│
├── Forgery_Detection/
│   ├── detect_forgery.py
│   └── output/
│
├── Risk_Engine/
│   ├── main.py
│   ├── merge.py
│   ├── risk_engine.py
│   ├── data/
│   │   ├── ocr_output.json
│   │   └── forgery_output.json
│   └── reports/
│       └── risk_report.json
│
├── Streamlit_UI/
│
├── Dataset/
│
└── README.md
```

---

## Workflow

```
Upload Documents
        │
        ▼
OCR Extraction
        │
        ▼
Forgery Detection
        │
        ▼
Merge OCR + Forgery Results
        │
        ▼
Cross Document Validation
        │
        ▼
Risk Score Calculation
        │
        ▼
Risk Report Generation
        │
        ▼
Dashboard & AI Explanation
```

---

## Risk Assessment Logic

The Risk Engine evaluates each application based on multiple parameters:

* OCR confidence
* Forgery score
* Tampering detection
* Name consistency across documents
* Cross-document validation

Based on these checks, every application is classified into one of three categories:

| Risk Score | Decision    |
| ---------- | ----------- |
| Low        | Low Risk    |
| Medium     | Medium Risk |
| High       | High Risk   |

---

## Sample Output

`''json
{
    "application_id": "tampered_003",
    "documents": 3,
    "name_validation": "FAIL",
    "risk_score": 235,
    "decision": "HIGH RISK",
    "reasons": [
        "High forgery score in salary_slip",
        "Tampering detected in salary_slip",
        "High forgery score in bank_statement",
        "Tampering detected in bank_statement",
        "High forgery score in property_document",
        "Tampering detected in property_document",
        "Name mismatch across documents"
    ]
}
```

---

## Technologies Used

* Python
* JSON
* OCR
* Streamlit
* Artificial Intelligence
* Document Processing
* Risk Analysis

---

## Team Contributions

### Member 1

* OCR Module
* Text Extraction
* Document Parsing

### Member 2

* Forgery Detection
* Tampering Detection
* Forgery Scoring

### Member 3

* Merge Engine
* Cross-Document Validation
* Risk Engine
* Risk Report Generation

### Member 4

* AI Explanation Layer
* Streamlit Dashboard
* User Interface
* Final System Integration

---

## Future Enhancements

* Real-time document verification
* Deep learning-based forgery detection
* Digital signature verification
* QR code validation
* Blockchain-based document authentication
* API integration with banking systems
* Multi-language document support


## License

This project is developed for educational purposes as part of the **Canara Bank Suraksha Cyber Hackathon**.
