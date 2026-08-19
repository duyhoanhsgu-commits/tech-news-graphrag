"""Top-level API router — aggregates all route modules."""
from __future__ import annotations

from fastapi import APIRouter

from graphrag.api.routes.admin import router as admin_router
from graphrag.api.routes.graph import router as graph_router
from graphrag.api.routes.health import router as health_router
from graphrag.api.routes.query import router as query_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(query_router, prefix="/query", tags=["query"])
api_router.include_router(graph_router, prefix="/graph", tags=["graph"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
