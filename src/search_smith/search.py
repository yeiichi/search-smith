"""High-level search helpers."""

from __future__ import annotations

from search_smith.models import SearchResult
from search_smith.providers.base import SearchProvider
from search_smith.providers.brave import BraveSearch


def search(
    query: str,
    *,
    count: int = 10,
    offset: int = 0,
    provider: SearchProvider | None = None,
) -> list[SearchResult]:
    """Search with the configured provider, defaulting to Brave Search."""
    if provider is not None:
        return provider.search(query, count=count, offset=offset)

    with BraveSearch() as brave:
        return brave.search(query, count=count, offset=offset)
