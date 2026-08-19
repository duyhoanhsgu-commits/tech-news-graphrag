"""Query endpoints — vector RAG and GraphRAG."""
from __future__ import annotations

from fastapi import APIRouter

from graphrag.schemas.query import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/graphrag", response_model=QueryResponse, summary="GraphRAG query")
async def graphrag_query(request: QueryRequest) -> QueryResponse:
    """Answer a question using hybrid vector + graph retrieval."""
    # TODO: inject and call GraphRAGPipeline
    raise NotImplementedError


@router.post("/vector", response_model=QueryResponse, summary="Vector-only RAG query")
async def vector_query(request: QueryRequest) -> QueryResponse:
    """Answer a question using vector-only retrieval."""
    # TODO: inject and call VectorRAGPipeline
    raise NotImplementedError
