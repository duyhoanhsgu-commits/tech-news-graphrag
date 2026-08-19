"""Graph inspection endpoints."""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/entities", summary="List entities")
async def list_entities(label: str | None = None, limit: int = 50) -> list[dict]:
    # TODO: query Neo4j repository
    raise NotImplementedError


@router.get("/entities/{entity_id}", summary="Get entity detail")
async def get_entity(entity_id: str) -> dict:
    raise NotImplementedError


@router.get("/entities/{entity_id}/neighbors", summary="Get entity neighbors")
async def get_neighbors(entity_id: str, max_hops: int = 1) -> dict:
    raise NotImplementedError
