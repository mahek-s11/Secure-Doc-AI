def get_person_name(doc):
    """
    Extract and normalize person's name
    from different document types.
    """

    if "employee_name" in doc:
        name = doc["employee_name"]

    elif "account_holder" in doc:
        name = doc["account_holder"]

    elif "owner_name" in doc:
        name = doc["owner_name"]

    else:
        return None

    name = name.replace("Employee", "Person")
    name = name.replace("Customer", "Person")
    name = name.replace("Owner", "Person")

    return name.strip()


def evaluate_applications(merged_documents):

    # -------------------------------
    # Group documents by application
    # -------------------------------

    applications = {}

    for doc in merged_documents:

        parts = doc["document_id"].split("_")

        status = parts[-2]
        number = parts[-1]

        application_id = f"{status}_{number}"

        if application_id not in applications:
            applications[application_id] = []

        applications[application_id].append(doc)

    print("Applications :", len(applications))

    print("\n========================================")
    print("CROSS DOCUMENT VALIDATION & RISK ENGINE")
    print("========================================")

    risk_reports = []

    # -------------------------------
    # Process every application
    # -------------------------------

    for app_id, docs in applications.items():

        print("\n----------------------------------------")
        print("Application :", app_id)

        names = []
        risk_score = 0
        reasons = []

        for doc in docs:

            person = get_person_name(doc)

            if person:
                names.append(person)

            # Forgery Detection

            if doc["forgery_score"] > 80:
                risk_score += 40
                reasons.append(
                    f"High forgery score in {doc['document_type']}"
                )

            # Tampering

            if doc["tampering_flag"]:
                risk_score += 30
                reasons.append(
                    f"Tampering detected in {doc['document_type']}"
                )

            # OCR Confidence

            if doc["ocr_confidence"] < 0.90:
                risk_score += 10
                reasons.append(
                    f"Low OCR confidence in {doc['document_type']}"
                )

        unique_names = set(names)

        if len(unique_names) == 1:

            print("Name Validation : PASS")

        else:

            print("Name Validation : FAIL")
            print("Names Found :", unique_names)

            risk_score += 25
            reasons.append("Name mismatch across documents")

        # Final Decision

        if risk_score < 30:
            decision = "LOW RISK"

        elif risk_score < 70:
            decision = "MEDIUM RISK"

        else:
            decision = "HIGH RISK"

        print("Risk Score :", risk_score)
        print("Decision :", decision)

        print("Reasons:")

        if len(reasons) == 0:
            print("✓ No suspicious activity detected")
            reasons.append("No suspicious activity detected")

        else:
            for reason in reasons:
                print("-", reason)

        report = {
            "application_id": app_id,
            "documents": len(docs),
            "name_validation": "PASS" if len(unique_names) == 1 else "FAIL",
            "risk_score": risk_score,
            "decision": decision,
            "reasons": reasons
        }

        risk_reports.append(report)

    return risk_reports