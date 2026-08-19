"""Unit tests for entity resolution (matcher + deduplicator)."""
from __future__ import annotations

import uuid

import pytest

from graphrag.graph.resolution.deduplicator import EntityDeduplicator
from graphrag.graph.resolution.entity_matcher import EntityMatcher
from graphrag.schemas.entity import Entity


def _make_entity(name: str, etype: str = "Organization") -> Entity:
    return Entity(entity_id=str(uuid.uuid4()), name=name, type=etype)


def test_exact_match_deduplicates() -> None:
    e1 = _make_entity("OpenAI")
    e2 = _make_entity("OpenAI")
    dedup = EntityDeduplicator()
    entities, _ = dedup.deduplicate([e1, e2], [])
    assert len(entities) == 1


def test_fuzzy_match_deduplicates() -> None:
    e1 = _make_entity("Google LLC")
    e2 = _make_entity("Google Llc")
    dedup = EntityDeduplicator(EntityMatcher(threshold=0.9))
    entities, _ = dedup.deduplicate([e1, e2], [])
    assert len(entities) == 1


def test_distinct_entities_kept() -> None:
    e1 = _make_entity("Apple")
    e2 = _make_entity("Microsoft")
    dedup = EntityDeduplicator()
    entities, _ = dedup.deduplicate([e1, e2], [])
    assert len(entities) == 2
