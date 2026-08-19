"""End-to-end GraphRAG pipeline integration test."""
from __future__ import annotations

import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_graphrag_pipeline_end_to_end() -> None:
    """Full pipeline: ingest → index → query → answer with citations."""
    pytest.skip("Requires live Postgres + Neo4j + OpenAI API key")
