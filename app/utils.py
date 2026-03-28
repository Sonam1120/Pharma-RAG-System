from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_chunks(documents):
    chunks = []
    metadata = []

    for doc in documents:
        sentences = doc["content"].split(".")
        for i, sent in enumerate(sentences):
            sent = sent.strip()
            if sent:
                chunks.append(sent)
                metadata.append({
                    "doc_id": doc["doc_id"],
                    "module": doc["module"],
                    "submodule": doc["submodule"],
                    "status": doc["status"],
                    "version": doc["version"],
                    "is_latest": doc["is_latest"],
                    "chunk_id": i,
                    "text": sent
                })

    return chunks, metadata


def create_index(chunks):
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index


def search(query, index, chunks, metadata, module=None, submodule=None):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k=3)

    results = []
    closest_docs = []

    for idx in I[0]:
        meta = metadata[idx]

        closest_docs.append(meta["doc_id"])

        if not (meta["status"] == "Approved" and meta["is_latest"]):
            continue

        if module and meta["module"] != module:
            continue

        if submodule and meta["submodule"] != submodule:
            continue

        results.append(meta)

    return results, list(set(closest_docs))


def generate_answer(query, retrieved_chunks, closest_docs):
    if not retrieved_chunks:
        return {
            "answer": "Insufficient evidence in approved documents.",
            "citations": [],
            "closest_docs": closest_docs[:3]
        }

    answer = ""
    citations = []

    for i, chunk in enumerate(retrieved_chunks):
        answer += f"{i+1}. {chunk['text']}. "

        citations.append({
            "doc_id": chunk["doc_id"],
            "chunk_id": chunk["chunk_id"],
            "snippet": chunk["text"]
        })

    return {
        "answer": answer.strip(),
        "citations": citations,
        "closest_docs": closest_docs[:3]
    }