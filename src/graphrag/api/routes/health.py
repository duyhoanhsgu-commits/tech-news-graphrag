"""Health-check endpoints."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    version: str


@router.get("", response_model=HealthResponse, summary="Liveness check")
async def health() -> HealthResponse:
    return HealthResponse(status="ok", version="0.1.0")


@router.get("/ready", response_model=HealthResponse, summary="Readiness check")
async def readiness() -> HealthResponse:
    # TODO: ping Postgres and Neo4j before returning ok
    return HealthResponse(status="ok", version="0.1.0")
