def filter_documents(docs, module=None, submodule=None):
    filtered = []

    for doc in docs:
        if doc["status"] != "Approved":
            continue
        
        if module and doc["module"] != module:
            continue
        
        if submodule and doc["submodule"] != submodule:
            continue
        
        filtered.append(doc)

    return filtered


def get_latest_versions(docs):
    latest = {}

    for doc in docs:
        if doc["id"] not in latest or doc["version"] > latest[doc["id"]]["version"]:
            latest[doc["id"]] = doc

    return list(latest.values())

from app.governance import apply_governance

def get_final_docs(query):
    
    retrieved_docs = get_relevant_docs(query)

    filtered_docs = apply_governance(retrieved_docs)

    return filtered_docs

def get_relevant_docs(query):
    
    documents = [
        {
            "doc_id": "DOC_1",
            "text": "MBR is used for batch manufacturing",
            "status": "Approved",
            "is_latest": True
        },
        {
            "doc_id": "DOC_2",
            "text": "Draft MBR should not be used",
            "status": "Draft",
            "is_latest": True
        },
        {
            "doc_id": "DOC_3",
            "text": "CAPA is corrective action",
            "status": "Approved",
            "is_latest": True
        }
    ]

    results = []

    for doc in documents:
        if query.lower() in doc["text"].lower():
            results.append(doc)

    return results