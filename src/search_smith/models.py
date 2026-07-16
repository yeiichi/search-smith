"""Provider-neutral search result models."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any


@dataclass(frozen=True, slots=True)
class SearchResult:
    """A normalized web search result."""

    title: str
    url: str
    snippet: str
    source: str
    rank: int
    score: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.title.strip():
            msg = "SearchResult title must not be empty."
            raise ValueError(msg)
        if not self.url.strip():
            msg = "SearchResult url must not be empty."
            raise ValueError(msg)
        if not self.source.strip():
            msg = "SearchResult source must not be empty."
            raise ValueError(msg)
        if self.rank < 1:
            msg = "SearchResult rank must be greater than or equal to 1."
            raise ValueError(msg)
        if self.score is not None and self.score < 0:
            msg = "SearchResult score must not be negative."
            raise ValueError(msg)

        object.__setattr__(self, "title", self.title.strip())
        object.__setattr__(self, "url", self.url.strip())
        object.__setattr__(self, "snippet", self.snippet.strip())
        object.__setattr__(self, "source", self.source.strip())
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    def to_dict(self) -> dict[str, Any]:
        """Return a stable JSON-serializable representation."""
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
            "rank": self.rank,
            "score": self.score,
            "metadata": dict(self.metadata),
        }
