"""Provider interface definitions."""

from __future__ import annotations

from typing import Protocol

from search_smith.models import SearchResult


class SearchProvider(Protocol):
    """Minimal protocol implemented by search providers."""

    def search(
        self,
        query: str,
        *,
        count: int = 10,
        offset: int = 0,
    ) -> list[SearchResult]:
        """Search for web results."""
