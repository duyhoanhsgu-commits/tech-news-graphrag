"""LLM extraction prompts for entities and relationships."""
from __future__ import annotations

ENTITY_EXTRACTION_SYSTEM = """\
You are an expert information-extraction assistant.
Extract named entities from the provided text.
Return a JSON array of objects with fields: name, type, description.
Allowed types: {entity_types}
Return ONLY valid JSON — no explanation, no markdown fences.\
"""

ENTITY_EXTRACTION_USER = """\
Text:
{text}

Extract entities:\
"""

RELATION_EXTRACTION_SYSTEM = """\
You are an expert relation-extraction assistant.
Given a list of entities and a text passage, identify relationships between entities.
Return a JSON array of objects with fields: source, target, relationship_type, description.
Allowed relationship types: RELATED_TO, WORKS_FOR, LOCATED_IN, ACQUIRED, COMPETES_WITH.
Return ONLY valid JSON — no explanation, no markdown fences.\
"""

RELATION_EXTRACTION_USER = """\
Entities:
{entities}

Text:
{text}

Extract relationships:\
"""
