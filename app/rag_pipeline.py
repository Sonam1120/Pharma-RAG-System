from app.ingestion import model
import numpy as np

def search(query, index, chunks):
    query_embedding = model.encode([query])
    
    D, I = index.search(np.array(query_embedding), k=5)
    
    results = []
    for i in I[0]:
        results.append(chunks[i])
    
    return results


def generate_answer(query, retrieved_chunks):
    if not retrieved_chunks:
        return "Insufficient evidence in approved documents"

    answer = " ".join(retrieved_chunks[:2])

    citations = []
    for i, chunk in enumerate(retrieved_chunks[:2]):
        citations.append({
            "chunk_id": i,
            "snippet": chunk[:100]
        })

    return {
        "answer": answer,
        "citations": citations
    }