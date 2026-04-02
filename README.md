# Pharma-RAG-System

<!-- this is only how to run project info -->

## Setup Instructions

### 1. Activate Virtual Environment

**Windows:**

```
cd venv
cd Scripts
activate
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Run Server

```
uvicorn app.main:app --reload
```

---

## API URLs

* Base URL: http://127.0.0.1:8000/
* Swagger UI: http://127.0.0.1:8000/docs

---

## How RAG Works

1. Documents are ingested from dataset
2. Data is split into chunks
3. Each chunk stores:

   * doc_id
   * text
   * status (Approved/Draft)
   * version (latest or not)
4. User query is received
5. Relevant documents are retrieved
6. Governance filter is applied
7. Answer is generated using filtered data

---

## Governance Logic

* Only **Approved documents** are used
* Only **latest version** is considered
* Draft or outdated documents are ignored

---

##  Refusal Logic

If no valid documents are found after governance filtering:

Response:

```
Insufficient evidence to answer
```

---

## Citations

Each response includes:

* `doc_id`
* `snippet` (text used to generate answer)

Example:

```
{
  "answer": "MBR is used for batch manufacturing",
  "citations": [
    {
      "doc_id": "DOC_1",
      "snippet": "MBR is used for batch manufacturing"
    }
  ]
}
```

---

## Evaluation Metrics

The following 4 metrics are implemented:

1. **Answer Accuracy (AA)**
2. **Hallucination Rate (HR)**
3. **Retrieval Recall@5 (R@5)**
4. **Citation Precision (CP)**

### Run evaluation:

```
python app/evaluation.py
```

---

## Example Queries

| Query | Expected Output       |
| ----- | --------------------- |
| MBR   | Correct Answer        |
| CAPA  | Correct Answer        |
| CEO   | Refusal               |
| Draft | Rejected (Governance) |

---

## Assumptions

* Sample dataset is used
* Keyword-based retrieval is implemented
* No external embedding API is used
* System is designed for demonstration purpose

---

## Project Structure

```
app/
│── main.py
│── retrieval.py
│── governance.py
│── rag_pipeline.py
│── evaluation.py
│── ingestion.py
│── models.py
│── schemas.py
│── utils.py

data/
│── sample_docs.json
│── questions.json

requirements.txt
README.md
```

---

## Features Implemented

✔ RAG Pipeline
✔ Governance Filter (Approved + latest)
✔ Refusal Logic
✔ Citations in Response
✔ Evaluation Metrics

---

<!-- detailed info -->


## Detailed Overview

This project implements a **Retrieval-Augmented Generation (RAG) system combined with Governance controls** for a Pharma Document Management System (DMS).

### Objective

To build a system that:

* Retrieves relevant information from documents
* Ensures **only Approved & latest documents** are used
* Generates **grounded answers (no hallucination)**
* Provides **traceable citations**
* Refuses when data is insufficient

---

## System Architecture (Step-by-Step)

### 1. Document Ingestion

* Source: `data/sample_docs.json`
* Each document contains:

  * `doc_id`
  * `text`
  * `status` → Approved / Draft
  * `is_latest` → True / False

Implemented in: `ingestion.py`

---

### 2. Chunking

* Documents are treated as chunks (simplified design)
* Each record = 1 chunk

 (Can be extended to sentence-level chunking)

---

### 3. Embedding & Indexing

* Instead of vector DB, used **keyword-based retrieval**
* Matching logic:

  * query.lower() in document text

 Implemented in: `retrieval.py`

---

### 4. Query Handling API

* Endpoint: `GET /query?q=`
* Input: user query
* Output:

  * answer
  * citations

 Implemented in: `main.py`

---

### 5. Retrieval Logic

* Fetch top matching documents
* Returns list of relevant docs

 Example:

```
Query: MBR
→ DOC_1 matched
```

---

### 6. Governance Filtering (CRITICAL)

Only allow:

* status = Approved
* is_latest = True

Reject:

* Draft docs
* Old versions

 Implemented in: `governance.py`

---

### 7. Answer Generation

* Answer is constructed using filtered docs
* No external LLM used (rule-based response)

 Implemented in: `rag_pipeline.py`

---

### 8. Citation Generation

Each answer includes:

* doc_id
* snippet

Example:

```json
{
  "doc_id": "DOC_1",
  "snippet": "MBR is used for batch manufacturing"
}
```

---

##  Refusal Logic (Very Important)

System refuses when:

* No documents found
* Only Draft docs found
* No Approved/latest data available

Response:

```json
{
  "answer": "Insufficient evidence to answer",
  "citations": []
}
```

---

## Evaluation Strategy (25 Questions)

Evaluation is done using predefined dataset:
 `data/questions.json`

---

### Metrics Implemented

#### 1. Answer Accuracy (AA)

* Measures correctness
* Scoring:

  * 1 → Correct
  * 0.5 → Partial
  * 0 → Wrong

---

#### 2. Hallucination Rate (HR)

* Checks unsupported claims
* If answer not backed by citation → hallucination

---

#### 3. Retrieval Recall@5 (R@5)

* Checks if correct doc is in top 5

---

#### 4. Citation Precision (CP)

* Checks if citation actually supports answer

---

###  Run Evaluation

```bash
python app/evaluation.py
```

---

## Example Queries & Expected Behavior

| Query | Behavior              |
| ----- | --------------------- |
| MBR   | Answer + Citation     |
| CAPA  | Answer + Citation     |
| CEO   | Refusal               |
| Draft | Rejected (Governance) |

---

## Assumptions

* Dataset is small and static
* No vector DB used
* No LLM API used
* Focus is on logic clarity and governance

---

## Project Structure (Detailed)

```
app/
│── main.py            # API endpoints
│── retrieval.py       # search logic
│── governance.py      # filtering rules
│── rag_pipeline.py    # pipeline orchestration
│── evaluation.py      # metrics calculation
│── ingestion.py       # load documents
│── models.py          # data structure
│── schemas.py         # request/response
│── utils.py           # helper functions

 data/
│── sample_docs.json   # documents
│── questions.json     # evaluation set

requirements.txt
README.md
```

---

## Bonus Implementations

* Modular code structure
* Clear separation of concerns
* Simple test dataset
* Easy to extend to vector DB (FAISS)

---

##  Final Summary

This project demonstrates:

* End-to-end **RAG pipeline**
* Strong **governance enforcement**
* **Grounded answers with citations**
* Proper **evaluation framework**

Designed to meet real-world Pharma compliance requirements.

