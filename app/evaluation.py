# ---------------------------
# Question Bank (Sample)
# ---------------------------
questions = [
    {"q": "What is MBR?", "expected_doc": "DOC_1", "should_refuse": False},
    {"q": "Should draft CAPA be implemented?", "expected_doc": None, "should_refuse": True},
    {"q": "What is GRN?", "expected_doc": "DOC_5", "should_refuse": False},
    {"q": "Who is company CEO?", "expected_doc": None, "should_refuse": True},
]

# ---------------------------
# Dummy Results (replace with actual outputs)
# ---------------------------
results = [
    {
        "question": "What is MBR?",
        "answer": "MBR is a document...",
        "citations": [{"doc_id": "DOC_1"}],
        "is_correct": 1,
        "hallucinated": False,
        "retrieved_docs": ["DOC_1", "DOC_2"]
    },
    {
        "question": "Should draft CAPA be implemented?",
        "answer": "Not allowed",
        "citations": [],
        "is_correct": 1,
        "hallucinated": False,
        "retrieved_docs": []
    },
]

# ---------------------------
# Metrics Calculation
# ---------------------------

def calculate_metrics(results):
    total = len(results)

    correct_answers = 0
    hallucinations = 0
    recall_hits = 0
    correct_citations = 0

    for res in results:
        # Accuracy
        correct_answers += res.get("is_correct", 0)

        # Hallucination
        if res.get("hallucinated", False):
            hallucinations += 1

        # Recall@5
        expected_doc = None
        for q in questions:
            if q["q"] == res["question"]:
                expected_doc = q["expected_doc"]

        if expected_doc and expected_doc in res.get("retrieved_docs", []):
            recall_hits += 1

        # Citation Precision
        citations = res.get("citations", [])
        if expected_doc:
            for c in citations:
                if c.get("doc_id") == expected_doc:
                    correct_citations += 1
                    break

    # Final Metrics
    accuracy = correct_answers / total if total else 0
    hallucination_rate = hallucinations / total if total else 0
    recall_at_5 = recall_hits / total if total else 0
    citation_precision = correct_citations / total if total else 0

    return {
        "Answer Accuracy": accuracy,
        "Hallucination Rate": hallucination_rate,
        "Recall@5": recall_at_5,
        "Citation Precision": citation_precision
    }

# 1. Answer Accuracy
accuracy = correct_answers / total_queries

# 2. Hallucination Rate
hallucination_rate = hallucinated_answers / total_queries

# 3. Retrieval Recall@5
recall_at_5 = retrieved_correct_docs / total_queries

# 4. Citation Precision
citation_precision = correct_citations / total_queries
# ---------------------------
# Run Evaluation
# ---------------------------
if __name__ == "__main__":
    metrics = calculate_metrics(results)

    print("📊 Evaluation Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {round(v, 2)}")

        