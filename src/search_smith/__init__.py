"""Public API for search-smith."""

from search_smith.exceptions import (
    AuthenticationError,
    ConfigurationError,
    ProviderError,
    RateLimitError,
    SearchSmithError,
)
from search_smith.models import SearchResult
from search_smith.providers.brave import BraveSearch
from search_smith.search import search

__all__ = [
    "AuthenticationError",
    "BraveSearch",
    "ConfigurationError",
    "ProviderError",
    "RateLimitError",
    "SearchResult",
    "SearchSmithError",
    "search",
]
