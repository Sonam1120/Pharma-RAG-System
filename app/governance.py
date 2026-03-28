def filter_approved_latest(docs):
    """
    Filters documents to include only:
    - status = Approved
    - is_latest = True
    """
    filtered_docs = []

    for doc in docs:
        if doc.get("status") == "Approved" and doc.get("is_latest") == True:
            filtered_docs.append(doc)

    return filtered_docs

def check_if_empty(docs):
    """
    Check if after governance no documents remain
    """
    if not docs:
        return True
    return False

def filter_docs(docs):
    return [
        doc for doc in docs
        if doc["status"] == "Approved" and doc["is_latest"] == True
    ]


def apply_governance(docs):
    if not docs:
        return []

    return [
        doc for doc in docs
        if doc.get("status") == "Approved" and doc.get("is_latest") == True
    ]