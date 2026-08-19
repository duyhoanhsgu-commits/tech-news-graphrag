"""Pydantic-settings configuration loaded from env + YAML overrides."""
from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ────────────────────────────────────────────────────────────────
    app_env: Literal["development", "staging", "production"] = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_debug: bool = False
    app_secret_key: str = "change-me"
    cors_allow_origins: list[str] = Field(default=["*"])

    # ── Database ───────────────────────────────────────────────────────────
    database_url: str = "postgresql+asyncpg://graphrag:changeme@localhost:5432/graphrag"
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_timeout: int = 30

    # ── Neo4j ──────────────────────────────────────────────────────────────
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "changeme"
    neo4j_database: str = "neo4j"

    # ── Embedding ──────────────────────────────────────────────────────────
    embedding_provider: Literal["openai", "huggingface", "sentence-transformers"] = "openai"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536
    embedding_batch_size: int = 512

    # ── LLM ───────────────────────────────────────────────────────────────
    llm_provider: Literal["openai", "anthropic", "google", "ollama"] = "openai"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 2048

    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"

    # ── Retrieval ─────────────────────────────────────────────────────────
    vector_top_k: int = 20
    graph_top_k: int = 10
    rerank_top_k: int = 5
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    cohere_api_key: str = ""

    # ── Ingestion ─────────────────────────────────────────────────────────
    dataset_name: str = "cc_news"
    dataset_split: str = "train"
    articles_limit: int = 5000
    chunk_size: int = 512
    chunk_overlap: int = 64

    # ── Graph extraction ──────────────────────────────────────────────────
    entity_types: str = "Person,Organization,Location,Technology,Product,Event"
    max_entities_per_chunk: int = 20
    graph_extraction_batch_size: int = 16

    # ── Logging ───────────────────────────────────────────────────────────
    log_level: str = "INFO"
    log_format: Literal["json", "text"] = "json"
    log_file: str = ""

    @property
    def entity_type_list(self) -> list[str]:
        return [t.strip() for t in self.entity_types.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()
