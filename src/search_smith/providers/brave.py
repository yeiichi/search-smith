"""Brave Search provider."""

from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any

import httpx

from search_smith.exceptions import (
    AuthenticationError,
    ConfigurationError,
    ProviderError,
    RateLimitError,
)
from search_smith.models import SearchResult

BRAVE_SEARCH_API_KEY_ENV = "BRAVE_SEARCH_API_KEY"
BRAVE_WEB_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"
BRAVE_MAX_COUNT = 20
BRAVE_MAX_OFFSET = 9
DEFAULT_TIMEOUT_SECONDS = 10.0


class BraveSearch:
    """Client for Brave's Web Search API."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        client: httpx.Client | None = None,
        base_url: str = BRAVE_WEB_SEARCH_URL,
    ) -> None:
        self._api_key = self._resolve_api_key(api_key)
        self._owns_client = client is None
        self._client = client or httpx.Client(timeout=timeout)
        self._base_url = base_url

    def __enter__(self) -> BraveSearch:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client when this instance owns it."""
        if self._owns_client:
            self._client.close()

    def search(
        self,
        query: str,
        *,
        count: int = 10,
        offset: int = 0,
    ) -> list[SearchResult]:
        """Search Brave Web Search and return normalized web results."""
        normalized_query = validate_search_inputs(query, count=count, offset=offset)
        response = self._request(normalized_query, count=count, offset=offset)
        payload = self._decode_response(response)
        return parse_web_results(payload)

    @staticmethod
    def _resolve_api_key(api_key: str | None) -> str:
        resolved = (
            api_key if api_key is not None else os.getenv(BRAVE_SEARCH_API_KEY_ENV)
        )
        if resolved is None or not resolved.strip():
            msg = (
                "Brave Search API key is required. Set BRAVE_SEARCH_API_KEY "
                "or pass api_key to BraveSearch()."
            )
            raise ConfigurationError(msg)
        return resolved.strip()

    def _request(self, query: str, *, count: int, offset: int) -> httpx.Response:
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self._api_key,
        }
        params = {
            "q": query,
            "count": count,
            "offset": offset,
            "result_filter": "web",
            "text_decorations": False,
        }
        try:
            response = self._client.get(self._base_url, params=params, headers=headers)
        except httpx.TimeoutException as exc:
            msg = "Brave Search request timed out."
            raise ProviderError(msg) from exc
        except httpx.HTTPError as exc:
            msg = "Brave Search request failed before a response was received."
            raise ProviderError(msg) from exc

        if response.status_code in {401, 403}:
            msg = "Brave Search rejected the API key."
            raise AuthenticationError(msg)
        if response.status_code == 429:
            msg = "Brave Search rate limit was reached."
            raise RateLimitError(msg)
        if response.status_code >= 400:
            msg = f"Brave Search returned HTTP {response.status_code}."
            raise ProviderError(msg)
        return response

    @staticmethod
    def _decode_response(response: httpx.Response) -> Mapping[str, Any]:
        try:
            payload = response.json()
        except ValueError as exc:
            msg = "Brave Search returned a malformed JSON response."
            raise ProviderError(msg) from exc
        if not isinstance(payload, Mapping):
            msg = "Brave Search returned an unexpected response shape."
            raise ProviderError(msg)
        return payload


def validate_search_inputs(query: str, *, count: int, offset: int) -> str:
    """Validate provider-neutral inputs plus Brave's documented limits."""
    normalized_query = query.strip()
    if not normalized_query:
        msg = "Search query must not be empty."
        raise ValueError(msg)
    if count < 1:
        msg = "Search count must be positive."
        raise ValueError(msg)
    if count > BRAVE_MAX_COUNT:
        msg = f"Search count must not exceed Brave's limit of {BRAVE_MAX_COUNT}."
        raise ValueError(msg)
    if offset < 0:
        msg = "Search offset must not be negative."
        raise ValueError(msg)
    if offset > BRAVE_MAX_OFFSET:
        msg = f"Search offset must not exceed Brave's limit of {BRAVE_MAX_OFFSET}."
        raise ValueError(msg)
    return normalized_query


def parse_web_results(payload: Mapping[str, Any]) -> list[SearchResult]:
    """Parse Brave web results into provider-neutral results."""
    web = payload.get("web")
    if web is None:
        return []
    if not isinstance(web, Mapping):
        msg = "Brave Search response field 'web' must be an object when present."
        raise ProviderError(msg)

    raw_results = web.get("results", [])
    if raw_results is None:
        return []
    if not isinstance(raw_results, list):
        msg = "Brave Search response field 'web.results' must be a list."
        raise ProviderError(msg)

    results: list[SearchResult] = []
    for index, item in enumerate(raw_results, start=1):
        if not isinstance(item, Mapping):
            msg = "Brave Search returned a non-object item in 'web.results'."
            raise ProviderError(msg)

        title = _as_text(item.get("title"))
        url = _as_text(item.get("url"))
        if not title or not url:
            msg = "Brave Search returned a web result without a title or URL."
            raise ProviderError(msg)

        metadata = {
            key: value
            for key, value in item.items()
            if key not in {"title", "url", "description"}
        }
        results.append(
            SearchResult(
                title=title,
                url=url,
                snippet=_as_text(item.get("description")),
                source="brave",
                rank=index,
                metadata=metadata,
            )
        )
    return results


def _as_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)
