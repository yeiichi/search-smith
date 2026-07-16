# search-smith

`search-smith` is a small, reusable web-search abstraction package. Version
0.1.0 supports Brave Search as the only functional provider while keeping the
public API provider-neutral.

## Background

Programmatic web search is often a small but important part of evidence
collection, fact-checking, and retrieval workflows. As older APIs such as
Google's Custom Search JSON API become harder to rely on for new projects,
applications need a thin layer that can normalize results without tying the
rest of the codebase to one provider. `search-smith` starts with Brave Search,
which provides public web results from Brave's independent search index, and
keeps the provider boundary small enough for future alternatives.

## Quick start

```bash
uv add search-smith
export BRAVE_SEARCH_API_KEY="..."
```

```python
from search_smith import search

results = search("Python semantic release", count=10)

for result in results:
    print(result.title)
    print(result.url)
```

You can also use the explicit Brave client:

```python
from search_smith import BraveSearch

client = BraveSearch()
results = client.search("Python semantic release")
```

The CLI is available as `search-smith`:

```bash
search-smith "Brave Search API" --count 5
search-smith "Brave Search API" --format json
```

Full documentation is in `docs/` and is intended to be published by Read the
Docs at <https://search-smith.readthedocs.io/>.
