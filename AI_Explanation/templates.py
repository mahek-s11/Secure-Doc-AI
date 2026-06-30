"""
=========================================================
Secure-Doc-AI
AI Explanation Module
Purpose:
This file contains all the text templates used by the
AI Explanation Layer.
No business logic should be written here.
The explanation.py file will import these templates and
fill them according to the Risk Engine output.
=========================================================
"""


# =========================================================
# LOW RISK TEMPLATES
# =========================================================

LOW_RISK_SUMMARY = (
    "Three submitted documents were successfully analysed. "
    "The verification process found no significant inconsistencies "
    "or indicators of document fraud."
)

LOW_RISK_EXPLANATION = (
    "The submitted documents passed the automated verification process. "
    "Name validation was successful, no forgery indicators were detected, "
    "and all available information appears internally consistent."
)

LOW_RISK_RECOMMENDATION = (
    "The application may proceed through the standard verification process. "
    "No additional manual investigation is required."
)

# =========================================================
# MEDIUM RISK TEMPLATES
# =========================================================

MEDIUM_RISK_SUMMARY = (
    "The submitted documents contain a small number of inconsistencies "
    "that require additional verification before further processing."
)

MEDIUM_RISK_EXPLANATION = (
    "Automated verification detected moderate inconsistencies that "
    "could not be fully validated. While these findings do not "
    "necessarily indicate fraud, additional review is recommended."
)

MEDIUM_RISK_RECOMMENDATION = (
    "Manual verification is recommended before the application "
    "is approved."
)

# =========================================================
# HIGH RISK TEMPLATES
# =========================================================

HIGH_RISK_SUMMARY = (
    "Multiple inconsistencies and document integrity issues were "
    "identified during automated verification. The submitted "
    "documents exhibit characteristics commonly associated with "
    "document tampering or fraudulent modification."
)

HIGH_RISK_EXPLANATION = (
    "The application has been classified as HIGH RISK because "
    "multiple forgery indicators, tampering evidence, and "
    "cross-document inconsistencies were detected during analysis."
)

HIGH_RISK_RECOMMENDATION = (
    "Manual verification is mandatory before loan approval. "
    "The submitted documents should be authenticated before "
    "any further processing."
)

# =========================================================
# NAME VALIDATION
# =========================================================

NAME_PASS = (
    "Applicant identity validation completed successfully. "
    "The applicant name is consistent across all submitted documents."
)

NAME_FAIL = (
    "Applicant identity validation failed. "
    "The applicant name is inconsistent across one or more submitted documents."
)

# =========================================================
# CONFIDENCE LEVELS
# =========================================================

LOW_CONFIDENCE = (
    "High confidence that the submitted documents are authentic."
)

MEDIUM_CONFIDENCE = (
    "Moderate confidence. Some findings require manual review."
)

HIGH_CONFIDENCE = (
    "High confidence that significant anomalies have been detected."
)

# =========================================================
# RISK LEVEL DESCRIPTIONS
# =========================================================

LOW_DESCRIPTION = (
    "The application presents minimal fraud risk based on the "
    "available verification results."
)

MEDIUM_DESCRIPTION = (
    "The application presents moderate fraud risk and requires "
    "additional verification."
)

HIGH_DESCRIPTION = (
    "The application presents a high probability of document fraud "
    "or tampering."
)

# =========================================================
# NEXT STEP SUGGESTIONS
# =========================================================

LOW_NEXT_STEPS = [
    "Proceed with the standard application workflow.",
    "Archive verification results.",
    "Continue normal loan processing."
]

MEDIUM_NEXT_STEPS = [
    "Perform manual verification.",
    "Cross-check applicant information.",
    "Request supporting documents if necessary."
]

HIGH_NEXT_STEPS = [
    "Verify applicant identity manually.",
    "Authenticate all submitted documents.",
    "Review original salary slip.",
    "Review original bank statement.",
    "Verify property ownership documents.",
    "Escalate the application to the fraud investigation team."
]

# =========================================================
# DEFAULT MESSAGE
# =========================================================

UNKNOWN_RISK_SUMMARY = (
    "The submitted application could not be classified because "
    "insufficient verification data was available."
)

UNKNOWN_RISK_EXPLANATION = (
    "The AI Explanation Layer could not generate a complete "
    "assessment because the risk category was unavailable."
)

UNKNOWN_RISK_RECOMMENDATION = (
    "Please verify that the Risk Engine generated a valid report "
    "before proceeding."
)