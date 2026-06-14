# Enterprise RAG Chatbot — Helpson
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-F06D2B?style=for-the-badge&logo=chroma&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI_gpt--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)

Built as a capstone project with PT Indonesia Epson Industry as the case 
study client, addressing a real manufacturing helpdesk problem: technical 
knowledge was siloed, helpdesk was flooded with repetitive questions, and 
all issue reporting was manual — risking production stopline.

**My role: AI Engineer** — owned the full RAG pipeline (retrieval, embedding, 
generation) and FastAPI service layer.

> Deployed on PT Epson Indonesia's internal intranet. A sanitized version 
> (no internal data) is available at: [Helpson v2 Demo](https://v2.epson-chatbot-demo.fiilabs.web.id/)

---

## Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | tester31004@fiilabs.web.id | rajamuda850 |
| Employee | tester31002@fiilabs.web.id | rajamuda850 |

---

## Results

| Metric | Result | Target |
|--------|--------|--------|
| Retrieval Precision@5 | 0.96 | ≥ 0.60 ✅ |
| Chatbot response time | 7s | ≤ 30s ✅ |
| FAQ search time | 1s | ≤ 10s ✅ |
| UAT pass rate | 94.3% | 100% |
| User satisfaction | 4.72 / 5.00 | — |
| Security (high-risk vulnerabilities) | 0 | 0 ✅ |

Validated by 12 real users (6 admin, 6 employees) at PT Indonesia Epson 
Industry via demo, observation, interview, and satisfaction survey.

| Component | Detail |
|-----------|--------|
| API layer | FastAPI — /health + /chat endpoints |
| Generation model | gpt-4o-mini |
| Embedding model | text-embedding-3-small |
| Vector store | Chroma (persisted to disk) |
| Python version | 3.11.x (recommended) |

---

## Architecture

```
[HTTP Client / Express.js]
          ↓
  [FastAPI Service :8000]
    GET  /health
    POST /chat
          ↓
  [Retrieval Layer]
    Chroma vector store
    OpenAI embeddings
          ↓
  [Generation Layer]
    gpt-4o-mini
    Context-grounded answer
```

### Request flow

```
POST /chat  { query, k }
    → similarity_search()       top-k chunks from Chroma
    → build_context()           numbered context block + sources
    → generate_answer()         grounded answer from gpt-4o-mini
    → { query, answer, sources }
```

---

## Project Structure

```
enterprise-rag-chatbot/
├── data/
│   ├── raw/                    input documents (.pdf, .docx, .txt)
│   ├── processed/
│   │   └── chunks.json         chunk inspection artifact
│   └── chroma/                 persisted vector store
├── src/
│   ├── config.py               central configuration
│   ├── core/
│   │   └── exceptions.py       shared exception types
│   ├── api/
│   │   ├── main.py             FastAPI app entrypoint
│   │   ├── routes/
│   │   │   ├── health.py       GET /health
│   │   │   └── chat.py         POST /chat
│   │   └── schemas/
│   │       ├── request.py      ChatRequest
│   │       └── response.py     ChatResponse, HealthResponse, ErrorResponse
│   ├── data/
│   │   ├── loader.py           document loading (.pdf, .docx, .txt)
│   │   └── chunker.py          text splitting + chunks.json artifact
│   ├── embedding/
│   │   ├── embedder.py         OpenAI embedding client
│   │   └── indexer.py          Chroma vector store init and indexing
│   ├── llm/
│   │   ├── context_builder.py  retrieved docs → formatted context string
│   │   ├── prompt_templates.py system prompt + user prompt builder
│   │   └── generator.py        gpt-4o-mini answer generation
│   ├── retrieval/
│   │   ├── retriever.py        similarity and MMR search
│   │   └── evaluator.py        Precision@K evaluation
│   └── utils/
│       └── logger.py           logger factory
├── tests/
│   ├── conftest.py             shared fixtures and document factory
│   ├── test_context_builder.py
│   ├── test_prompt_templates.py
│   ├── test_generator.py
│   ├── test_api_health.py
│   ├── test_api_chat.py
│   ├── test_e2e_rag_pipeline.py
│   └── test_openai_connection.py
├── requirements.txt
├── requirements.lock           deterministic dependency tree
├── pyproject.toml
└── .python-version
```

---

## Setup

### Prerequisites

- Python 3.11.x (recommended for production) or 3.14.3 (dev environment)
- An OpenAI API key

> **Note:** This project was developed on Python 3.14.3 (pre-release).
> Python 3.11.x or 3.12.x is recommended for production deployments
> due to broader package wheel availability.

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd enterprise-rag-chatbot

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate.bat       # Windows

# Install dependencies from the lock file (deterministic)
pip install -r requirements.lock

# Install the package in editable mode
pip install -e .
```

### Environment variables

Create a `.env` file in the repo root:

```env
OPENAI_API_KEY=sk-...
APP_ENV=development
LOG_LEVEL=DEBUG
```

---

## Indexing Documents

Place your documents in `data/raw/`. Supported formats: `.pdf`, `.docx`, `.txt`.

```bash
# Step 1 — chunk documents and write inspection artifact
python src/data/chunker.py

# Step 2 — embed chunks and persist to Chroma
python src/embedding/indexer.py
```

After indexing, `data/processed/chunks.json` contains the chunked text
for inspection and `data/chroma/` contains the persisted vector store.

---

## Running the API

```bash
python -m uvicorn src.api.main:app --reload
```

The service starts on `http://localhost:8000`.

Interactive API docs: `http://localhost:8000/docs`

---

## API Reference

### `GET /health`

Returns service status, Chroma document count, and OpenAI reachability.

**Response**

```json
{
  "status": "ok",
  "chroma_doc_count": 263,
  "openai_reachable": true,
  "python_version": "3.11.9",
  "app_env": "development"
}
```

Status is `"degraded"` if OpenAI is unreachable or no documents are indexed.

**PowerShell**

```powershell
(Invoke-WebRequest -Uri http://localhost:8000/health).Content | python -m json.tool
```

---

### `POST /chat`

Accepts a query and returns a grounded answer with source citations.

**Request body**

```json
{
  "query": "How do I replace the ink cartridge?",
  "k": 5
}
```

| Field   | Type    | Required | Default | Constraints       |
| ------- | ------- | -------- | ------- | ----------------- |
| `query` | string  | Yes      | —       | 1–2000 characters |
| `k`     | integer | No       | 5       | 1–20              |

**Response**

```json
{
  "query": "How do I replace the ink cartridge?",
  "answer": "To replace the ink cartridge, open the printer cover... [1][2]",
  "sources": [
    {
      "file_name": "manual L3210.pdf",
      "file_path": "/data/raw/manual L3210.pdf",
      "chunk_index": 42
    }
  ]
}
```

**Error responses**

| Status | Condition                                          |
| ------ | -------------------------------------------------- |
| 404    | No relevant documents found for the query          |
| 422    | Invalid request body (empty query, k out of range) |
| 503    | Answer generation failed                           |
| 500    | Unexpected internal error                          |

