"""Application-wide exception hierarchy."""
from __future__ import annotations


class GraphRAGError(Exception):
    """Base exception for all application errors."""


# ── Ingestion ─────────────────────────────────────────────────────────────────
class IngestionError(GraphRAGError):
    """Raised when article loading or normalisation fails."""


class DatasetNotFoundError(IngestionError):
    """Raised when the requested HuggingFace dataset cannot be found."""


# ── Embedding ─────────────────────────────────────────────────────────────────
class EmbeddingError(GraphRAGError):
    """Raised when embedding generation fails."""


class EmbeddingProviderError(EmbeddingError):
    """Raised on upstream API errors from the embedding provider."""


# ── Vector store ──────────────────────────────────────────────────────────────
class VectorStoreError(GraphRAGError):
    """Raised on pgvector operation failures."""


# ── Graph ─────────────────────────────────────────────────────────────────────
class GraphError(GraphRAGError):
    """Raised on Neo4j operation failures."""


class EntityExtractionError(GraphError):
    """Raised when LLM entity extraction fails."""


# ── Retrieval ─────────────────────────────────────────────────────────────────
class RetrievalError(GraphRAGError):
    """Raised when retrieval returns no results or fails."""


# ── Generation ────────────────────────────────────────────────────────────────
class GenerationError(GraphRAGError):
    """Raised when LLM answer generation fails."""


class LLMProviderError(GenerationError):
    """Raised on upstream API errors from the LLM provider."""


# ── Configuration ─────────────────────────────────────────────────────────────
class ConfigurationError(GraphRAGError):
    """Raised when required configuration is missing or invalid."""
