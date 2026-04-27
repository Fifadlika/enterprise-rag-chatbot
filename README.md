# Enterprise RAG Chatbot

A retrieval-augmented generation (RAG) API for enterprise documents.
Retrieves relevant document chunks from a vector store and generates
grounded answers using OpenAI. Designed to be consumed by any HTTP
client — including an Express.js backend.

---

## Current Status

| Metric                | Value                               |
| --------------------- | ----------------------------------- |
| Retrieval Precision@5 | 0.96 (target ≥ 0.60) ✅             |
| API layer             | FastAPI — health + chat endpoints   |
| Generation model      | gpt-4o-mini                         |
| Embedding model       | text-embedding-3-small              |
| Vector store          | Chroma (persisted to disk)          |
| Python version        | 3.11.x (recommended) / 3.14.3 (dev) |

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

**PowerShell**

```powershell
(Invoke-WebRequest `
  -Uri http://localhost:8000/chat `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"query": "How do I replace the ink cartridge?", "k": 5}' `
).Content | python -m json.tool
```

**curl**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I replace the ink cartridge?", "k": 5}'
```

---

## Express.js Integration

The FastAPI service is designed to be consumed by an Express backend.
Express does not need to know anything about Python, LangChain, or Chroma —
it makes a standard HTTP POST and receives a JSON response.

```javascript
// Example Express route calling the RAG service
app.post("/api/chat", async (req, res) => {
  const { query, k = 5 } = req.body;

  const ragResponse = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, k }),
  });

  if (!ragResponse.ok) {
    const error = await ragResponse.json();
    return res.status(ragResponse.status).json(error);
  }

  const data = await ragResponse.json();
  res.json(data);
});
```

In production, replace `http://localhost:8000` with the internal
service address of the FastAPI container.

---

## Running Tests

```bash
# Full test suite
pytest tests/ -v

# With coverage report
pytest tests/ --cov=src --cov-report=term-missing

# Single test file
pytest tests/test_e2e_rag_pipeline.py -v
```

No `OPENAI_API_KEY` is required to run the test suite.
All external calls are mocked.

---

## Retrieval Evaluation

```bash
python src/retrieval/evaluator.py
```

Runs Precision@K against the hardcoded test query set and reports
pass/fail against the ≥ 0.60 threshold.

---

## Known Issues and Deferred Items

| Item                                                            | Severity | Target  |
| --------------------------------------------------------------- | -------- | ------- |
| `CHROMA_PERSIST_DIR` path inconsistency with `DATA_RAW_DIR`     | Major    | Phase 2 |
| Import strategy inconsistency in pre-Phase 0 modules            | Major    | Phase 2 |
| No unit tests for loader, chunker, embedder, indexer, retriever | Major    | Phase 2 |
| Evaluator uses hardcoded keyword heuristics                     | Medium   | Phase 2 |
| No API authentication                                           | Critical | Phase 3 |
| No containerization (Dockerfile)                                | Major    | Phase 3 |
| No structured logging with correlation IDs                      | Medium   | Phase 2 |
| Python 3.14.3 is pre-release — not recommended for production   | Major    | Phase 3 |

---

## Roadmap

| Phase   | Focus                                                              | Status     |
| ------- | ------------------------------------------------------------------ | ---------- |
| Phase 0 | Import cleanup, path normalization                                 | ✅ Done    |
| Phase 1 | API layer, LLM generation, end-to-end pipeline                     | ✅ Done    |
| Phase 2 | Hybrid retrieval, expanded metrics, unit tests, structured logging | 🔲 Planned |
| Phase 3 | Auth, containerization, CI pipeline, production hardening          | 🔲 Planned |
