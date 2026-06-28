import json

from merge import merge_documents
from risk_engine import evaluate_applications

# =====================================
# LOAD OCR DATA
# =====================================

with open("data/ocr_output.json", "r") as file:
    ocr_data = json.load(file)

# =====================================
# LOAD FORGERY DATA
# =====================================

with open("data/forgery_output.json", "r") as file:
    forgery_data = json.load(file)

documents = ocr_data["documents"]

print("OCR Documents :", len(documents))
print("Forgery Documents :", len(forgery_data))

# =====================================
# MERGE DOCUMENTS
# =====================================

merged_documents = merge_documents(
    documents,
    forgery_data
)

print("Merged Documents :", len(merged_documents))

# =====================================
# RUN RISK ENGINE
# =====================================

risk_reports = evaluate_applications(
    merged_documents
)

# =====================================
# SAVE REPORT
# =====================================

with open("reports/risk_report.json", "w") as file:
    json.dump(risk_reports, file, indent=4)

print("\n========================================")
print("Risk Report Saved Successfully!")
print("Location : reports/risk_report.json")
print("========================================")