def merge_documents(ocr_documents, forgery_documents):
    """
    Merge OCR output with forgery detection output
    using document_id.
    """

    merged_documents = []

    for ocr_doc in ocr_documents:

        for forgery_doc in forgery_documents:

            if ocr_doc["document_id"] == forgery_doc["document_id"]:

                merged_doc = {**ocr_doc, **forgery_doc}
                merged_documents.append(merged_doc)
                break

    return merged_documents