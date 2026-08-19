"""Admin endpoints — index management."""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post("/reindex", summary="Trigger full re-index")
async def reindex() -> dict:
    # TODO: trigger indexing pipeline as background task
    return {"status": "accepted"}


@router.delete("/reset", summary="Reset all indexes and graph data")
async def reset() -> dict:
    # TODO: call reset_database logic
    return {"status": "accepted"}
