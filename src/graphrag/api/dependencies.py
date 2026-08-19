"""FastAPI dependency providers."""
from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from graphrag.core.config import Settings, get_settings


def settings_dep() -> Settings:
    return get_settings()


SettingsDep = Annotated[Settings, Depends(settings_dep)]
