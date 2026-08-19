"""Application-wide constants."""
from __future__ import annotations

# Vector search
DEFAULT_VECTOR_TOP_K: int = 20
DEFAULT_RERANK_TOP_K: int = 5
MAX_CONTEXT_TOKENS: int = 4096

# Chunking
DEFAULT_CHUNK_SIZE: int = 512
DEFAULT_CHUNK_OVERLAP: int = 64

# Graph
DEFAULT_MAX_HOPS: int = 2
DEFAULT_SIMILARITY_THRESHOLD: float = 0.85

# API
API_V1_PREFIX: str = "/api/v1"
REQUEST_TIMEOUT_SECONDS: int = 60

# Data paths
RAW_DATA_DIR: str = "data/raw"
PROCESSED_DIR: str = "data/processed"
ARTICLES_DIR: str = "data/processed/articles"
CHUNKS_DIR: str = "data/processed/chunks"
ENTITIES_DIR: str = "data/processed/entities"
RELATIONSHIPS_DIR: str = "data/processed/relationships"
EVALUATION_DIR: str = "data/evaluation"
