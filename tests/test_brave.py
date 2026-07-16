import httpx
import pytest

from search_smith import (
    AuthenticationError,
    BraveSearch,
    ConfigurationError,
    ProviderError,
    RateLimitError,
)
from search_smith.providers.brave import BRAVE_SEARCH_API_KEY_ENV


def make_client(response: httpx.Response) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return response

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_successful_result_parsing() -> None:
    client = make_client(
        httpx.Response(
            200,
            json={
                "web": {
                    "results": [
                        {
                            "title": "Python Semantic Release",
                            "url": "https://python-semantic-release.readthedocs.io/",
                            "description": "Automated versioning.",
                            "age": "1 week",
                            "profile": {"name": "Docs"},
                        }
                    ]
                }
            },
        )
    )

    results = BraveSearch(api_key="key", client=client).search("release")

    assert len(results) == 1
    assert results[0].title == "Python Semantic Release"
    assert results[0].url == "https://python-semantic-release.readthedocs.io/"
    assert results[0].snippet == "Automated versioning."
    assert results[0].source == "brave"
    assert results[0].rank == 1
    assert results[0].metadata == {"age": "1 week", "profile": {"name": "Docs"}}


def test_missing_optional_brave_fields() -> None:
    client = make_client(
        httpx.Response(
            200,
            json={"web": {"results": [{"title": "Example", "url": "https://e.test"}]}},
        )
    )

    results = BraveSearch(api_key="key", client=client).search("example")

    assert results[0].snippet == ""
    assert results[0].metadata == {}


@pytest.mark.parametrize("payload", [{"web": {"results": []}}, {}, {"web": None}])
def test_empty_results(payload: dict[str, object]) -> None:
    client = make_client(httpx.Response(200, json=payload))

    assert BraveSearch(api_key="key", client=client).search("example") == []


def test_api_key_resolution_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["token"] = request.headers["X-Subscription-Token"]
        return httpx.Response(200, json={"web": {"results": []}})

    monkeypatch.setenv(BRAVE_SEARCH_API_KEY_ENV, "env-key")
    client = httpx.Client(transport=httpx.MockTransport(handler))

    BraveSearch(client=client).search("example")

    assert captured["token"] == "env-key"


def test_explicit_api_key_overrides_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["token"] = request.headers["X-Subscription-Token"]
        return httpx.Response(200, json={"web": {"results": []}})

    monkeypatch.setenv(BRAVE_SEARCH_API_KEY_ENV, "env-key")
    client = httpx.Client(transport=httpx.MockTransport(handler))

    BraveSearch(api_key="explicit-key", client=client).search("example")

    assert captured["token"] == "explicit-key"


def test_missing_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(BRAVE_SEARCH_API_KEY_ENV, raising=False)

    with pytest.raises(ConfigurationError, match="BRAVE_SEARCH_API_KEY"):
        BraveSearch()


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"query": "   "}, "query"),
        ({"count": 0}, "positive"),
        ({"count": 21}, "limit"),
        ({"offset": -1}, "negative"),
        ({"offset": 10}, "limit"),
    ],
)
def test_invalid_inputs(kwargs: dict[str, object], message: str) -> None:
    client = make_client(httpx.Response(200, json={"web": {"results": []}}))
    query = str(kwargs.pop("query", "example"))

    with pytest.raises(ValueError, match=message):
        BraveSearch(api_key="key", client=client).search(query, **kwargs)


def test_authentication_failure() -> None:
    client = make_client(httpx.Response(401, json={"error": {"detail": "bad key"}}))

    with pytest.raises(AuthenticationError, match="rejected"):
        BraveSearch(api_key="key", client=client).search("example")


def test_rate_limiting() -> None:
    client = make_client(httpx.Response(429, json={"error": {"detail": "limit"}}))

    with pytest.raises(RateLimitError, match="rate limit"):
        BraveSearch(api_key="key", client=client).search("example")


def test_generic_provider_failure() -> None:
    client = make_client(httpx.Response(500, json={"error": {"detail": "server"}}))

    with pytest.raises(ProviderError, match="HTTP 500"):
        BraveSearch(api_key="key", client=client).search("example")


@pytest.mark.parametrize(
    "response",
    [
        httpx.Response(200, content=b"not json"),
        httpx.Response(200, json=[]),
        httpx.Response(200, json={"web": []}),
        httpx.Response(200, json={"web": {"results": {}}}),
        httpx.Response(200, json={"web": {"results": [None]}}),
        httpx.Response(200, json={"web": {"results": [{"title": "No URL"}]}}),
    ],
)
def test_malformed_or_unexpected_responses(response: httpx.Response) -> None:
    client = make_client(response)

    with pytest.raises(ProviderError):
        BraveSearch(api_key="key", client=client).search("example")


def test_timeout_or_network_failure() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("timeout")

    client = httpx.Client(transport=httpx.MockTransport(handler))

    with pytest.raises(ProviderError, match="timed out"):
        BraveSearch(api_key="key", client=client).search("example")


def test_request_uses_brave_parameters() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json={"web": {"results": []}})

    client = httpx.Client(transport=httpx.MockTransport(handler))

    BraveSearch(api_key="key", client=client).search("example", count=5, offset=2)

    assert captured["params"] == {
        "q": "example",
        "count": "5",
        "offset": "2",
        "result_filter": "web",
        "text_decorations": "false",
    }
