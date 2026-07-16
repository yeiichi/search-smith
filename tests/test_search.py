from search_smith import SearchResult, search


class FakeProvider:
    def search(
        self,
        query: str,
        *,
        count: int = 10,
        offset: int = 0,
    ) -> list[SearchResult]:
        return [
            SearchResult(
                title=query,
                url="https://example.com",
                snippet=f"{count}:{offset}",
                source="fake",
                rank=1,
            )
        ]


def test_search_accepts_injected_provider() -> None:
    results = search("query", count=3, offset=1, provider=FakeProvider())

    assert results[0].title == "query"
    assert results[0].snippet == "3:1"
    assert results[0].source == "fake"
