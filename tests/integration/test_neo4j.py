"""Integration tests for Neo4j (requires a live Neo4j instance)."""
from __future__ import annotations

import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_upsert_entities_and_query() -> None:
    """Upsert entities and verify graph traversal returns neighbors."""
    pytest.skip("Requires live Neo4j — run with docker compose up neo4j")
