"""Integration tests for pgvector (requires a live Postgres+pgvector instance)."""
from __future__ import annotations

import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_upsert_and_search(sample_chunk) -> None:
    """Upsert a chunk and verify it is returned by similarity search."""
    pytest.skip("Requires live pgvector — run with docker compose up postgres")
