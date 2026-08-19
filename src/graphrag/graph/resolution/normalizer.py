"""Entity name normalizer for resolution pipeline."""
from __future__ import annotations

import re
import unicodedata


class EntityNameNormalizer:
    def normalize(self, name: str) -> str:
        name = unicodedata.normalize("NFKC", name)
        name = re.sub(r"\s+", " ", name)
        return name.strip().lower()
