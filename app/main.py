from fastapi import FastAPI
import json
from app.utils import create_chunks, create_index, search, generate_answer
from app.schemas import QueryRequest
from datetime import datetime

app = FastAPI()

# Load data
with open("data/sample_docs.json") as f:
    documents = json.load(f)

# Prepare chunks + index
chunks, metadata = create_chunks(documents)
index = create_index(chunks)

# Query logs (in-memory)
query_logs = []

@app.get("/")
def home():
    return {"message": "Pharma RAG API running"}


@app.post("/query")
def query_rag(request: QueryRequest):
    query = request.query

    retrieved, closest_docs = search(
        query,
        index,
        chunks,
        metadata,
        module=request.module,
        submodule=request.submodule
    )

    # pass closest_docs
    result = generate_answer(query, retrieved, closest_docs)

    query_logs.append({
        "query": query,
        "retrieved_docs": list(set([r["doc_id"] for r in retrieved])),
        "timestamp": str(datetime.now())
    })

    return {
        "answer": result["answer"],
        "citations": result["citations"],
        "closest_docs": result.get("closest_docs", []),
        "applied_filters": {
            "module": request.module,
            "submodule": request.submodule,
            "status": "Approved",
            "latest": True
        }
    }

@app.get("/logs")
def get_logs():
    return query_logs

@app.get("/metrics")
def get_metrics():
    total_queries = len(query_logs)

    # simple logic
    correct_answers = sum(
        1 for q in query_logs if "Insufficient evidence" not in q.get("answer", "")
    )
    refusals = total_queries - correct_answers

    accuracy = correct_answers / total_queries if total_queries > 0 else 0

    return {
        "total_queries": total_queries,
        "correct_answers": correct_answers,
        "refusals": refusals,
        "accuracy": round(accuracy, 2)
    }



