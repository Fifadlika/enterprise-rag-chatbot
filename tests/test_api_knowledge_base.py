# tests/test_api_knowledge_base.py
"""
Unit tests for POST /knowledge-base.

All external calls (loader, chunker, indexer, Chroma) are mocked.
No OPENAI_API_KEY required.
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from langchain.schema import Document

from src.api.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "doc_id": "doc-uuid-001",
    "file_path": "/data/uploads/report.pdf",
    "file_name": "report.pdf",
}

MOCK_CHUNKS = [
    Document(page_content=f"chunk {i}", metadata={"chunk_index": i})
    for i in range(3)
]


# ── Helpers ──────────────────────────────────────────────────────────────────

def _no_conflict_collection():
    """Chroma collection mock that reports doc_id as absent."""
    col = MagicMock()
    col.get.return_value = {"ids": []}
    return col


def _conflict_collection():
    """Chroma collection mock that reports doc_id as already present."""
    col = MagicMock()
    col.get.return_value = {"ids": ["some-vector-id"]}
    return col


def _mock_vector_store(collection_mock):
    vs = MagicMock()
    vs._collection = collection_mock
    return vs


# ── 400: file not found ───────────────────────────────────────────────────────

def test_post_kb_file_not_found():
    with patch("src.api.routes.knowledge_base.Path") as MockPath:
        MockPath.return_value.exists.return_value = False
        MockPath.return_value.suffix.lower.return_value = ".pdf"

        resp = client.post("/knowledge-base", json=VALID_PAYLOAD)

    assert resp.status_code == 400
    assert "FILE_NOT_FOUND" in resp.headers.get("x-error-code", "")


# ── 400: unsupported file type ────────────────────────────────────────────────

def test_post_kb_unsupported_file_type():
    with patch("src.api.routes.knowledge_base.Path") as MockPath, \
         patch("src.api.routes.knowledge_base.load_single_document", return_value=[]):

        MockPath.return_value.exists.return_value = True
        MockPath.return_value.suffix.lower.return_value = ".xyz"

        resp = client.post("/knowledge-base", json=VALID_PAYLOAD)

    assert resp.status_code == 400
    assert "UNSUPPORTED_FILE_TYPE" in resp.headers.get("x-error-code", "")


# ── 409: doc_id already indexed ───────────────────────────────────────────────

def test_post_kb_doc_id_conflict():
    mock_vs = _mock_vector_store(_conflict_collection())

    with patch("src.api.routes.knowledge_base.Path") as MockPath, \
         patch("src.api.routes.knowledge_base.load_single_document",
               return_value=[Document(page_content="x", metadata={})]), \
         patch("src.api.routes.knowledge_base.get_vector_store",
               return_value=mock_vs):

        MockPath.return_value.exists.return_value = True
        MockPath.return_value.suffix.lower.return_value = ".pdf"

        resp = client.post("/knowledge-base", json=VALID_PAYLOAD)

    assert resp.status_code == 409
    assert "DOC_ID_CONFLICT" in resp.headers.get("x-error-code", "")


# ── 500: unexpected indexing failure ─────────────────────────────────────────

def test_post_kb_indexing_failure():
    mock_vs = _mock_vector_store(_no_conflict_collection())

    with patch("src.api.routes.knowledge_base.Path") as MockPath, \
         patch("src.api.routes.knowledge_base.load_single_document",
               return_value=[Document(page_content="x", metadata={})]), \
         patch("src.api.routes.knowledge_base.get_vector_store",
               return_value=mock_vs), \
         patch("src.api.routes.knowledge_base.chunk_documents",
               return_value=MOCK_CHUNKS), \
         patch("src.api.routes.knowledge_base.index_documents",
               side_effect=Exception("Chroma exploded")):

        MockPath.return_value.exists.return_value = True
        MockPath.return_value.suffix.lower.return_value = ".pdf"

        resp = client.post("/knowledge-base", json=VALID_PAYLOAD)

    assert resp.status_code == 500
    assert "INDEXING_FAILED" in resp.headers.get("x-error-code", "")


# ── 200: happy path ───────────────────────────────────────────────────────────

def test_post_kb_success():
    mock_vs = _mock_vector_store(_no_conflict_collection())

    with patch("src.api.routes.knowledge_base.Path") as MockPath, \
         patch("src.api.routes.knowledge_base.load_single_document",
               return_value=[Document(page_content="content", metadata={})]), \
         patch("src.api.routes.knowledge_base.get_vector_store",
               return_value=mock_vs), \
         patch("src.api.routes.knowledge_base.chunk_documents",
               return_value=MOCK_CHUNKS), \
         patch("src.api.routes.knowledge_base.index_documents",
               return_value=mock_vs):

        MockPath.return_value.exists.return_value = True
        MockPath.return_value.suffix.lower.return_value = ".pdf"

        resp = client.post("/knowledge-base", json=VALID_PAYLOAD)

    assert resp.status_code == 200
    body = resp.json()
    assert body["doc_id"] == VALID_PAYLOAD["doc_id"]
    assert body["file_name"] == VALID_PAYLOAD["file_name"]
    assert body["chunks_indexed"] == len(MOCK_CHUNKS)
    assert body["status"] == "indexed"