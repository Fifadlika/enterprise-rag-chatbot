# src/api/routes/knowledge_base.py
"""
Knowledge Base management endpoints.

POST   /knowledge-base          — load, chunk, and index a single document
DELETE /knowledge-base/{doc_id} — remove all vectors for a document
"""
from pathlib import Path

from fastapi import APIRouter, HTTPException
from langchain.schema import Document

from src.api.schemas.knowledge_base import (
    AddKnowledgeBaseRequest,
    AddKnowledgeBaseResponse,
    DeleteKnowledgeBaseResponse,
)
from src.data.loader import load_single_document
from src.data.chunker import chunk_documents
from src.embedding.indexer import get_vector_store, index_documents
from src.utils.logger import get_logger

logger = get_logger("src.api.routes.knowledge_base")

router = APIRouter()


def _doc_id_exists(doc_id: str) -> tuple[bool, int]:
    """
    Check whether any vectors carrying the given doc_id are already in Chroma.

    Returns:
        (exists: bool, count: int) — count is 0 when exists is False.

    Note:
        Uses the same private _collection accessor pattern as
        get_collection_count(). Flagged as Phase 3 cleanup target.
    """
    vector_store = get_vector_store()
    result = vector_store._collection.get(
        where={"doc_id": doc_id},
        limit=1,
    )
    count = len(result.get("ids", []))
    return count > 0, count


@router.post(
    "/knowledge-base",
    response_model=AddKnowledgeBaseResponse,
    status_code=200,
    summary="Index a new document into the knowledge base",
)
def add_knowledge_base(request: AddKnowledgeBaseRequest) -> AddKnowledgeBaseResponse:
    """
    Load, chunk, and index a single document.

    The Express backend is responsible for:
    - Generating doc_id (UUID)
    - Saving the file to shared storage
    - Sending file_path to this endpoint

    Error codes:
        FILE_NOT_FOUND       — file_path does not exist on disk
        UNSUPPORTED_FILE_TYPE — file extension not in {.txt, .pdf, .docx}
        DOC_ID_CONFLICT      — doc_id is already present in Chroma
        INDEXING_FAILED      — unexpected failure during embedding/storage
    """
    logger.info(
        f"POST /knowledge-base | doc_id={request.doc_id!r} "
        f"file_name={request.file_name!r}"
    )

    # Guard 1: file must exist on disk
    if not Path(request.file_path).exists():
        logger.warning(f"File not found: {request.file_path!r}")
        raise HTTPException(
            status_code=400,
            detail=f"File not found: {request.file_path}",
            headers={"X-Error-Code": "FILE_NOT_FOUND"},
        )

    # Guard 2: load document — empty return means unsupported extension
    documents = load_single_document(request.file_path)
    if not documents:
        logger.warning(
            f"Unsupported file type for {request.file_name!r}. "
            f"Extension: {Path(request.file_path).suffix.lower()!r}"
        )
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {Path(request.file_path).suffix.lower()}. "
                "Supported formats: .txt, .pdf, .docx"
            ),
            headers={"X-Error-Code": "UNSUPPORTED_FILE_TYPE"},
        )

    # Guard 3: doc_id must not already be indexed
    exists, _ = _doc_id_exists(request.doc_id)
    if exists:
        logger.warning(f"doc_id already indexed: {request.doc_id!r}")
        raise HTTPException(
            status_code=409,
            detail=f"doc_id already indexed: {request.doc_id}",
            headers={"X-Error-Code": "DOC_ID_CONFLICT"},
        )

    # Happy path: chunk and index
    try:
        chunks: list[Document] = chunk_documents(documents)
        index_documents(chunks, doc_id=request.doc_id)
    except Exception as exc:
        logger.exception(
            f"Indexing failed for doc_id={request.doc_id!r}: {exc}"
        )
        raise HTTPException(
            status_code=500,
            detail="Unexpected failure during document indexing.",
            headers={"X-Error-Code": "INDEXING_FAILED"},
        )

    logger.info(
        f"Indexed doc_id={request.doc_id!r} | "
        f"{len(chunks)} chunks | file={request.file_name!r}"
    )

    return AddKnowledgeBaseResponse(
        doc_id=request.doc_id,
        file_name=request.file_name,
        chunks_indexed=len(chunks),
        status="indexed",
    )