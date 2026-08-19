"""Fuzzy entity matcher — groups entity mentions by name similarity."""
from __future__ import annotations

from difflib import SequenceMatcher

from graphrag.graph.resolution.normalizer import EntityNameNormalizer
from graphrag.schemas.entity import Entity


class EntityMatcher:
    def __init__(self, threshold: float = 0.85) -> None:
        self._threshold = threshold
        self._normalizer = EntityNameNormalizer()

    def match(self, entities: list[Entity]) -> dict[str, str]:
        """Returns {entity_id: canonical_entity_id} mapping."""
        canonical: dict[str, Entity] = {}
        mapping: dict[str, str] = {}
        for entity in entities:
            norm = self._normalizer.normalize(entity.name)
            matched = self._find_match(norm, canonical)
            if matched:
                mapping[entity.entity_id] = matched.entity_id
            else:
                canonical[norm] = entity
                mapping[entity.entity_id] = entity.entity_id
        return mapping

    def _find_match(
        self,
        name: str,
        canonical: dict[str, Entity],
    ) -> Entity | None:
        for canon_name, entity in canonical.items():
            ratio = SequenceMatcher(None, name, canon_name).ratio()
            if ratio >= self._threshold:
                return entity
        return None
