from types import MappingProxyType

import pytest

from search_smith import SearchResult


def test_search_result_trims_values_and_freezes_metadata() -> None:
    result = SearchResult(
        title=" Example ",
        url=" https://example.com ",
        snippet=" snippet ",
        source=" brave ",
        rank=1,
        metadata={"age": "1 day"},
    )

    assert result.title == "Example"
    assert result.url == "https://example.com"
    assert result.snippet == "snippet"
    assert result.source == "brave"
    assert isinstance(result.metadata, MappingProxyType)
    assert result.to_dict()["metadata"] == {"age": "1 day"}


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"title": ""}, "title"),
        ({"url": ""}, "url"),
        ({"source": ""}, "source"),
        ({"rank": 0}, "rank"),
        ({"score": -1.0}, "score"),
    ],
)
def test_search_result_rejects_invalid_values(
    kwargs: dict[str, object], message: str
) -> None:
    base = {
        "title": "Title",
        "url": "https://example.com",
        "snippet": "",
        "source": "brave",
        "rank": 1,
    }
    base.update(kwargs)

    with pytest.raises(ValueError, match=message):
        SearchResult(**base)
